from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from textual.app import ComposeResult
from textual.containers import Horizontal, Vertical
from textual.reactive import reactive
from textual.widgets import Static

from bloom import __version__
from bloom.cli.textual_ui.widgets.banner.bee import Bee
from bloom.cli.textual_ui.widgets.no_markup_static import NoMarkupStatic
from bloom.core.config import BloomConfig
from bloom.core.skills.manager import SkillManager


@dataclass
class BannerState:
    active_model: str = ""
    active_model_display: str = ""
    models_count: int = 0
    mcp_servers_count: int = 0
    skills_count: int = 0


class Banner(Static):
    state = reactive(BannerState(), init=False)

    def __init__(
        self, config: BloomConfig, skill_manager: SkillManager, **kwargs: Any
    ) -> None:
        super().__init__(**kwargs)
        self.can_focus = False
        self._initial_state = self._build_state(config, skill_manager)
        self._animated = not config.disable_welcome_banner_animation

    def compose(self) -> ComposeResult:
        with Horizontal(id="banner-container"):
            yield Bee(animate=self._animated)

            with Vertical(id="banner-info"):
                with Horizontal(classes="banner-line"):
                    yield NoMarkupStatic("Bloom", id="banner-brand")
                    yield NoMarkupStatic(" ", classes="banner-spacer")
                    yield NoMarkupStatic(f"v{__version__} · ", classes="banner-meta")
                    yield NoMarkupStatic("", id="banner-model")
                with Horizontal(classes="banner-line"):
                    yield NoMarkupStatic("", id="banner-meta-counts")
                with Horizontal(classes="banner-line"):
                    yield NoMarkupStatic("Type ", classes="banner-meta")
                    yield NoMarkupStatic("/help", classes="banner-cmd")
                    yield NoMarkupStatic(" for more information", classes="banner-meta")

    def on_mount(self) -> None:
        self.state = self._initial_state

    def watch_state(self) -> None:
        display = self.state.active_model_display or self.state.active_model
        self.query_one("#banner-model", NoMarkupStatic).update(display)
        self.query_one("#banner-meta-counts", NoMarkupStatic).update(
            self._format_meta_counts()
        )

    def freeze_animation(self) -> None:
        if self._animated:
            self.query_one(Bee).freeze_animation()

    @staticmethod
    def _build_state(config: BloomConfig, skill_manager: SkillManager) -> BannerState:
        display = config.active_model
        try:
            display = config.get_active_model().display_name
        except ValueError:
            pass
        return BannerState(
            active_model=config.active_model,
            active_model_display=display,
            models_count=len(config.models),
            mcp_servers_count=len(config.mcp_servers),
            skills_count=len(skill_manager.available_skills),
        )

    def set_state(self, config: BloomConfig, skill_manager: SkillManager) -> None:
        self.state = self._build_state(config, skill_manager)

    def _format_meta_counts(self) -> str:
        return (
            f"{self.state.models_count} model{'s' if self.state.models_count != 1 else ''}"
            f" · {self.state.mcp_servers_count} MCP server{'s' if self.state.mcp_servers_count != 1 else ''}"
            f" · {self.state.skills_count} skill{'s' if self.state.skills_count != 1 else ''}"
        )
