from __future__ import annotations

import time

import pytest
from textual.widgets import Button

from bloom.cli.textual_ui.app import BloomApp, ChatScroll
from bloom.cli.textual_ui.widgets.load_more import (
    HistoryLoadMoreMessage,
    HistoryLoadMoreRequested,
)
from bloom.cli.textual_ui.widgets.messages import UserMessage
from bloom.cli.textual_ui.windowing import (
    HISTORY_RESUME_TAIL_MESSAGES,
    LOAD_MORE_BATCH_SIZE,
)
from bloom.core.config import BloomConfig, SessionLoggingConfig
from bloom.core.types import LLMMessage, Role
from tests.conftest import build_test_agent_loop


@pytest.fixture
def bloom_config() -> BloomConfig:
    return BloomConfig(
        session_logging=SessionLoggingConfig(enabled=False), enable_update_checks=False
    )


async def _wait_until(pause, predicate, timeout: float = 2.0) -> None:
    start = time.monotonic()
    while (time.monotonic() - start) < timeout:
        if predicate():
            return
        await pause(0.02)
    raise AssertionError("Condition was not met within the timeout")


async def _wait_for_load_more(app: BloomApp, pause) -> None:
    await _wait_until(
        pause, lambda: len(app.query(HistoryLoadMoreMessage)) == 1, timeout=5.0
    )


def _load_more_remaining(app: BloomApp) -> int:
    label = app.query_one(HistoryLoadMoreMessage).query_one(Button).label
    text = str(label)
    _, _, remainder = text.rpartition("(")
    return int(remainder.rstrip(")"))


@pytest.mark.asyncio
async def test_ui_session_incremental_loader_shows_tail_and_load_more(
    bloom_config: BloomConfig,
) -> None:
    agent_loop = build_test_agent_loop(config=bloom_config, enable_streaming=False)
    agent_loop.messages.extend([
        LLMMessage(role=Role.user, content=f"msg-{idx}") for idx in range(66)
    ])

    app = BloomApp(agent_loop=agent_loop)

    async with app.run_test() as pilot:
        await _wait_until(
            pilot.pause,
            lambda: len(app.query(UserMessage)) == HISTORY_RESUME_TAIL_MESSAGES,
            timeout=5.0,
        )
        await _wait_for_load_more(app, pilot.pause)

        assert len(app.query(UserMessage)) == HISTORY_RESUME_TAIL_MESSAGES
        load_more = app.query_one(HistoryLoadMoreMessage)
        label = load_more.query_one(Button).label
        assert "(" in str(label)


@pytest.mark.asyncio
async def test_ui_session_incremental_loader_load_more_shows_remaining_count(
    bloom_config: BloomConfig,
) -> None:
    total_messages = 31
    agent_loop = build_test_agent_loop(config=bloom_config, enable_streaming=False)
    agent_loop.messages.extend([
        LLMMessage(role=Role.user, content=f"msg-{idx}")
        for idx in range(total_messages)
    ])

    app = BloomApp(agent_loop=agent_loop)

    async with app.run_test() as pilot:
        await _wait_until(
            pilot.pause,
            lambda: len(app.query(UserMessage)) == HISTORY_RESUME_TAIL_MESSAGES,
            timeout=5.0,
        )
        await _wait_for_load_more(app, pilot.pause)

        initial_remaining = total_messages - HISTORY_RESUME_TAIL_MESSAGES
        assert _load_more_remaining(app) == initial_remaining

        app.post_message(HistoryLoadMoreRequested())
        expected_remaining = initial_remaining - LOAD_MORE_BATCH_SIZE
        await _wait_until(
            pilot.pause,
            lambda: _load_more_remaining(app) == expected_remaining,
            timeout=5.0,
        )


@pytest.mark.asyncio
async def test_ui_session_incremental_loader_load_more_batches_until_done(
    bloom_config: BloomConfig,
) -> None:
    agent_loop = build_test_agent_loop(config=bloom_config, enable_streaming=False)
    agent_loop.messages.extend([
        LLMMessage(role=Role.user, content=f"msg-{idx}") for idx in range(31)
    ])

    app = BloomApp(agent_loop=agent_loop)

    async with app.run_test() as pilot:
        await _wait_until(
            pilot.pause,
            lambda: len(app.query(UserMessage)) == HISTORY_RESUME_TAIL_MESSAGES,
            timeout=5.0,
        )
        await _wait_for_load_more(app, pilot.pause)

        total_messages = 31
        while len(app.query(HistoryLoadMoreMessage)) == 1:
            current_count = len(app.query(UserMessage))
            app.post_message(HistoryLoadMoreRequested())
            await _wait_until(
                pilot.pause,
                lambda current_count=current_count: len(app.query(UserMessage))
                > current_count,
            )

        await _wait_until(
            pilot.pause, lambda: len(app.query(UserMessage)) == total_messages
        )


@pytest.mark.asyncio
async def test_ui_session_incremental_loader_keeps_top_alignment_when_not_scrollable(
    bloom_config: BloomConfig,
) -> None:
    agent_loop = build_test_agent_loop(config=bloom_config, enable_streaming=False)
    agent_loop.messages.extend([
        LLMMessage(role=Role.user, content=f"msg-{idx}")
        for idx in range(HISTORY_RESUME_TAIL_MESSAGES + 1)
    ])

    app = BloomApp(agent_loop=agent_loop)

    async with app.run_test(size=(120, 80)) as pilot:
        await _wait_for_load_more(app, pilot.pause)
        chat = app.query_one("#chat", ChatScroll)
        assert chat.max_scroll_y == 0
        assert chat.scroll_y == 0
