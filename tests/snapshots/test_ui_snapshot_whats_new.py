from __future__ import annotations

import os
from pathlib import Path
import time
from unittest.mock import patch

from textual.pilot import Pilot

from bloom.cli.update_notifier import UpdateCache
from tests.snapshots.base_snapshot_test_app import BaseSnapshotTestApp, default_config
from tests.snapshots.snap_compare import SnapCompare
from tests.update_notifier.adapters.fake_update_cache_repository import (
    FakeUpdateCacheRepository,
)
from tests.update_notifier.adapters.fake_update_gateway import FakeUpdateGateway


class SnapshotTestAppWithWhatsNew(BaseSnapshotTestApp):
    def __init__(self):
        self._previous_api_key = os.environ.get("POLLINATIONS_API_KEY")
        os.environ["POLLINATIONS_API_KEY"] = "snapshot-api-key"

        config = default_config()
        config.enable_update_checks = False
        update_notifier = FakeUpdateGateway(update=None)
        cache = UpdateCache(
            latest_version="1.0.0",
            stored_at_timestamp=int(time.time()),
            seen_whats_new_version=None,
        )
        update_cache_repository = FakeUpdateCacheRepository(update_cache=cache)
        super().__init__(
            config=config,
            update_notifier=update_notifier,
            update_cache_repository=update_cache_repository,
            current_version="1.0.0",
        )

    def on_unmount(self) -> None:
        if self._previous_api_key is None:
            os.environ.pop("POLLINATIONS_API_KEY", None)
        else:
            os.environ["POLLINATIONS_API_KEY"] = self._previous_api_key
        return None


class SnapshotTestAppWithPlanUpgradeCTA(SnapshotTestAppWithWhatsNew):
    pass


class SnapshotTestAppWithSwitchKeyCTA(SnapshotTestAppWithWhatsNew):
    pass


class SnapshotTestAppWithWhatsNewNoPlanCTA(SnapshotTestAppWithWhatsNew):
    pass


def test_snapshot_shows_whats_new_message(
    snap_compare: SnapCompare, tmp_path: Path
) -> None:
    # Create whats_new.md file before the app starts
    whats_new_file = tmp_path / "whats_new.md"
    whats_new_file.write_text("# What's New\n\n- Feature 1\n- Feature 2\n- Feature 3")

    async def run_before(pilot: Pilot) -> None:
        await pilot.pause(0.5)

    with patch("bloom.cli.update_notifier.whats_new.BLOOM_ROOT", tmp_path):
        assert snap_compare(
            "test_ui_snapshot_whats_new.py:SnapshotTestAppWithWhatsNew",
            terminal_size=(120, 36),
            run_before=run_before,
        )


def test_snapshot_shows_upgrade_message(
    snap_compare: SnapCompare, tmp_path: Path
) -> None:
    whats_new_file = tmp_path / "whats_new.md"
    whats_new_file.write_text("# What's New\n\n- Feature 1\n- Feature 2\n- Feature 3")

    async def run_before(pilot: Pilot) -> None:
        await pilot.pause(0.5)

    with patch("bloom.cli.update_notifier.whats_new.BLOOM_ROOT", tmp_path):
        assert snap_compare(
            "test_ui_snapshot_whats_new.py:SnapshotTestAppWithPlanUpgradeCTA",
            terminal_size=(120, 36),
            run_before=run_before,
        )


def test_snapshot_shows_switch_message(
    snap_compare: SnapCompare, tmp_path: Path
) -> None:
    whats_new_file = tmp_path / "whats_new.md"
    whats_new_file.write_text("# What's New\n\n- Feature 1\n- Feature 2\n- Feature 3")

    async def run_before(pilot: Pilot) -> None:
        await pilot.pause(0.5)

    with patch("bloom.cli.update_notifier.whats_new.BLOOM_ROOT", tmp_path):
        assert snap_compare(
            "test_ui_snapshot_whats_new.py:SnapshotTestAppWithSwitchKeyCTA",
            terminal_size=(120, 36),
            run_before=run_before,
        )


def test_snapshot_shows_no_plan_message(
    snap_compare: SnapCompare, tmp_path: Path
) -> None:
    whats_new_file = tmp_path / "whats_new.md"
    whats_new_file.write_text("# What's New\n\n- Feature 1\n- Feature 2\n- Feature 3")

    async def run_before(pilot: Pilot) -> None:
        await pilot.pause(0.5)

    with patch("bloom.cli.update_notifier.whats_new.BLOOM_ROOT", tmp_path):
        assert snap_compare(
            "test_ui_snapshot_whats_new.py:SnapshotTestAppWithWhatsNewNoPlanCTA",
            terminal_size=(120, 36),
            run_before=run_before,
        )
