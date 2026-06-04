import importlib.util
import sys
import types
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load_main_module():
    requests_module = types.ModuleType("requests")
    requests_module.post = lambda *args, **kwargs: None
    sys.modules.setdefault("requests", requests_module)

    github_module = types.ModuleType("github")
    github_module.Github = object
    github_module.Auth = types.SimpleNamespace(Token=lambda token: token)
    sys.modules.setdefault("github", github_module)

    github_exception_module = types.ModuleType("github.GithubException")
    github_exception_module.UnknownObjectException = type(
        "UnknownObjectException", (Exception,), {}
    )
    sys.modules.setdefault("github.GithubException", github_exception_module)

    openai_module = types.ModuleType("openai")
    openai_module.OpenAI = object
    sys.modules.setdefault("openai", openai_module)

    spec = importlib.util.spec_from_file_location(
        "update_tracker_main", ROOT / "scripts" / "main.py"
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class FakeDeepSeekClient:
    def __init__(self):
        self.calls = []
        self.chat = types.SimpleNamespace(
            completions=types.SimpleNamespace(create=self._create)
        )

    def _create(self, **kwargs):
        self.calls.append(kwargs)
        return types.SimpleNamespace(
            choices=[
                types.SimpleNamespace(
                    message=types.SimpleNamespace(content="generated report")
                )
            ]
        )


def make_commit():
    return types.SimpleNamespace(
        sha="abcdef1234567890",
        html_url="https://github.example/commit/abcdef1",
        commit=types.SimpleNamespace(message="Add Nanite renderer update"),
        files=[
            types.SimpleNamespace(filename="Engine/Source/Runtime/Renderer/File.cpp")
        ],
    )


class AnalyzeCommitsTests(unittest.TestCase):
    def test_analyze_commits_uses_deepseek_chat_completion_response_text(self):
        main = load_main_module()
        client = FakeDeepSeekClient()

        report = main.analyze_commits_in_bulk(
            client, "deepseek-v4-flash", [make_commit()], "Chinese"
        )

        self.assertEqual(report, "generated report")
        self.assertEqual(len(client.calls), 1)
        call = client.calls[0]
        self.assertEqual(call["model"], "deepseek-v4-flash")
        self.assertFalse(call["stream"])
        self.assertEqual(call["messages"][0]["role"], "user")
        prompt = call["messages"][0]["content"]
        self.assertIn("Chinese", prompt)
        self.assertIn("abcdef1", prompt)
        self.assertIn("Add Nanite renderer update", prompt)
        self.assertIn("Engine/Source/Runtime/Renderer/File.cpp", prompt)


if __name__ == "__main__":
    unittest.main()
