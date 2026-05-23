import os
import unittest
from unittest.mock import patch, MagicMock
import tempfile

import audio_transcriber_server


class TestTranscribeAudio(unittest.TestCase):

    def setUp(self):
        os.environ["OPENROUTER_API_KEY"] = "test-key"

    def tearDown(self):
        os.environ.pop("OPENROUTER_API_KEY", None)

    @patch("audio_transcriber_server.httpx.post")
    def test_transcribe_success(self, mock_post):
        mock_response = MagicMock()
        mock_response.json.return_value = {"text": "jom kita cuba soalan baru"}
        mock_post.return_value = mock_response

        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
            f.write(b"\x00" * 1000)
            tmp = f.name
        try:
            result = audio_transcriber_server.transcribe_audio(tmp)
            self.assertEqual(result, "jom kita cuba soalan baru")
        finally:
            os.unlink(tmp)

        mock_post.assert_called_once()
        _, kwargs = mock_post.call_args
        self.assertIn("input_audio", kwargs["json"])
        self.assertEqual(kwargs["json"]["model"], "openai/whisper-large-v3-turbo")
        self.assertEqual(kwargs["json"]["input_audio"]["format"], "wav")

    @patch("audio_transcriber_server.httpx.post")
    def test_http_error(self, mock_post):
        mock_response = MagicMock()
        mock_response.raise_for_status.side_effect = Exception("API Error")
        mock_post.return_value = mock_response

        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
            f.write(b"\x00" * 1000)
            tmp = f.name
        try:
            with self.assertRaises(Exception):
                audio_transcriber_server.transcribe_audio(tmp)
        finally:
            os.unlink(tmp)

    def test_missing_file(self):
        with self.assertRaises(FileNotFoundError):
            audio_transcriber_server.transcribe_audio("/nonexistent/path.wav")

    def test_missing_api_key(self):
        del os.environ["OPENROUTER_API_KEY"]
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
            f.write(b"\x00" * 1000)
            tmp = f.name
        try:
            with self.assertRaises(ValueError):
                audio_transcriber_server.transcribe_audio(tmp)
        finally:
            os.unlink(tmp)

    @patch("audio_transcriber_server.httpx.post")
    def test_audio_encoded_as_base64(self, mock_post):
        mock_response = MagicMock()
        mock_response.json.return_value = {"text": "test"}
        mock_post.return_value = mock_response

        payload = b"fake wav content"
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
            f.write(payload)
            tmp = f.name
        try:
            audio_transcriber_server.transcribe_audio(tmp)
        finally:
            os.unlink(tmp)

        import base64
        _, kwargs = mock_post.call_args
        sent_data = kwargs["json"]["input_audio"]["data"]
        expected = base64.b64encode(payload).decode("utf-8")
        self.assertEqual(sent_data, expected)


if __name__ == "__main__":
    unittest.main()
