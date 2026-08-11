import asyncio
from types import SimpleNamespace

from vikingbot.cli import commands


class _CompletedChannelManager:
    async def start_all(self) -> None:
        await asyncio.sleep(0)


class _IdleAgentLoop:
    async def run(self) -> None:
        await asyncio.Event().wait()

    async def close_mcp(self) -> None:
        pass


def test_eval_chat_does_not_create_cron_store(monkeypatch, tmp_path):
    config = SimpleNamespace(bot_data_path=tmp_path / "bot")

    monkeypatch.setattr(commands, "ensure_config", lambda _path: config)
    monkeypatch.setattr(commands, "validate_openviking_auth", lambda _config: None)
    monkeypatch.setattr(commands, "_warn_deprecated_memory_user", lambda _users: None)
    monkeypatch.setattr(commands, "_init_bot_data", lambda _config: None)
    monkeypatch.setattr(commands, "_redirect_openviking_logs_to_stderr", lambda: None)
    monkeypatch.setattr(commands, "get_data_dir", lambda: tmp_path)
    monkeypatch.setattr(commands, "SessionManager", lambda _path: object())
    monkeypatch.setattr(
        commands,
        "prepare_agent_channel",
        lambda *_args, **_kwargs: _CompletedChannelManager(),
    )
    monkeypatch.setattr(
        commands,
        "prepare_agent_loop",
        lambda *_args, **_kwargs: _IdleAgentLoop(),
    )
    monkeypatch.setattr(
        commands,
        "logger",
        SimpleNamespace(remove=lambda: None, add=lambda *_args, **_kwargs: None),
    )

    commands.chat(
        message="evaluation question",
        session_id="eval-session",
        markdown=False,
        logs=False,
        eval=True,
        config_path=None,
        sender=None,
        memory_peer=None,
        memory_user=None,
    )

    assert not (tmp_path / "cron" / "jobs.json").exists()
