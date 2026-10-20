import contextlib
import importlib.util
import io
import os
from pathlib import Path
import subprocess
import sys
import unittest
from unittest.mock import Mock, patch

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "weibo-hot-search-analysis"
sys.path.insert(0, str(SKILL))
spec = importlib.util.spec_from_file_location("weibo_client", SKILL / "api-client.py")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
Client = module.WeiboHotSearchClient


class CredentialTests(unittest.TestCase):
    def setUp(self):
        network = patch.object(module.requests.Session, "request", side_effect=AssertionError("NETWORK_DISABLED"))
        network.start()
        self.addCleanup(network.stop)

    def test_missing_or_placeholder_key_fails_before_session_creation(self):
        for value in [None, "", "  ", "YOUR_OWN_API_KEY", "your_tianapi_key_here"]:
            with self.subTest(value=value), patch.dict(os.environ, {}, clear=True):
                if value is not None:
                    os.environ["TIANAPI_KEY"] = value
                with patch.object(module.requests, "Session") as session:
                    with self.assertRaisesRegex(ValueError, "TIANAPI_KEY"):
                        Client()
                    session.assert_not_called()

    def test_key_is_loaded_at_runtime_and_passed_as_params(self):
        with patch.dict(os.environ, {"TIANAPI_KEY": "offline-unit-test-key"}):
            client = Client()
        self.assertNotIn("offline-unit-test-key", client.endpoint)
        response = Mock(status_code=200)
        response.json.return_value = {"result": {"list": [{"hotword": "测试", "hotwordnum": "1,234"}]}}
        with patch.object(client.session, "get", return_value=response) as get:
            topics = client.fetch_hot_search()
        self.assertEqual(topics[0]["heat"], 1234)
        self.assertEqual(get.call_args.kwargs["params"], {"key": "offline-unit-test-key"})
        self.assertFalse(get.call_args.kwargs["allow_redirects"])

    def test_explicit_key_has_precedence(self):
        with patch.dict(os.environ, {"TIANAPI_KEY": "env-test-key"}):
            client = Client(api_key="argument-test-key")
        with patch.object(client.session, "get", side_effect=module.requests.RequestException("private")) as get:
            with contextlib.redirect_stdout(io.StringIO()):
                client.fetch_hot_search()
        self.assertEqual(get.call_args.kwargs["params"], {"key": "argument-test-key"})

    def test_custom_url_credentials_are_rejected_without_echoing_them(self):
        for url in ["https://example.com/?key=offline-secret", "https://example.com/?access_token=offline-secret", "https://user:offline-secret@example.com/", "http://example.com/"]:
            with self.subTest(url=url):
                with self.assertRaises(ValueError) as error:
                    Client(endpoint=url)
                self.assertNotIn("offline-secret", str(error.exception))

    def test_uncredentialed_https_endpoint_needs_no_tianapi_key(self):
        with patch.dict(os.environ, {}, clear=True):
            client = Client(endpoint="https://example.com/hot?limit=10")
        with patch.object(client.session, "get", side_effect=module.requests.RequestException("private")) as get:
            with contextlib.redirect_stdout(io.StringIO()):
                client.fetch_hot_search()
        self.assertEqual(get.call_args.kwargs["params"], {})

    def test_request_and_json_errors_never_print_exception_text(self):
        for error in [module.requests.RequestException("https://example.com/?key=offline-secret"), ValueError("offline-secret")]:
            with self.subTest(error=type(error).__name__):
                client = Client(api_key="offline-secret")
                output = io.StringIO()
                with patch.object(client.session, "get", side_effect=error), contextlib.redirect_stdout(output):
                    self.assertEqual(client.fetch_hot_search(), [])
                self.assertNotIn("offline-secret", output.getvalue())
                self.assertNotIn("https://", output.getvalue())

    def test_redirects_are_not_parsed_or_followed(self):
        client = Client(api_key="offline-unit-test-key")
        response = Mock(status_code=302)
        with patch.object(client.session, "get", return_value=response), contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(client.fetch_hot_search(), [])
        response.json.assert_not_called()

    def test_provider_failure_is_not_a_fake_topic(self):
        client = Client(api_key="offline-unit-test-key")
        response = Mock(status_code=200)
        response.json.return_value = {"code": 401, "msg": "offline-secret"}
        output = io.StringIO()
        with patch.object(client.session, "get", return_value=response), contextlib.redirect_stdout(output):
            self.assertEqual(client.fetch_hot_search(), [])
        self.assertNotIn("offline-secret", output.getvalue())

    def test_save_failure_is_reported_and_cli_exits_nonzero(self):
        client = Client(api_key="offline-unit-test-key")
        output = io.StringIO()
        with patch("builtins.open", side_effect=OSError("offline-secret")), contextlib.redirect_stdout(output):
            self.assertIs(client.save_to_json([], "test-output.json"), False)
        self.assertNotIn("offline-secret", output.getvalue())
        fake = Mock()
        fake.fetch_hot_search.return_value = [{"rank": 1, "topic": "测试", "heat": 1}]
        fake.save_to_json.return_value = False
        output = io.StringIO()
        with patch.object(module, "WeiboHotSearchClient", return_value=fake), contextlib.redirect_stdout(output):
            self.assertEqual(module.main(), 1)
        self.assertNotIn("成功获取", output.getvalue())

    def test_cli_missing_key_exits_nonzero_without_traceback(self):
        env = dict(os.environ)
        env.pop("TIANAPI_KEY", None)
        env["PYTHONIOENCODING"] = "utf-8"
        runner = "import runpy, sys; from pathlib import Path; from unittest.mock import patch; import requests; sys.path.insert(0, str(Path(sys.argv[1]).parent))\nwith patch.object(requests.Session, 'request', side_effect=AssertionError('NETWORK_DISABLED')):\n runpy.run_path(sys.argv[1], run_name='__main__')"
        run = subprocess.run([sys.executable, "-c", runner, str(SKILL / "api-client.py")], env=env, capture_output=True, text=True, encoding="utf-8")
        self.assertEqual(run.returncode, 2)
        self.assertIn("TIANAPI_KEY", run.stdout + run.stderr)
        self.assertNotIn("Traceback", run.stdout + run.stderr)


if __name__ == "__main__":
    unittest.main()
