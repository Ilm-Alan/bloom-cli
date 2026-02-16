from __future__ import annotations

import random
from typing import Any

from textual.app import ComposeResult
from textual.timer import Timer
from textual.widgets import Static

from bloom.cli.textual_ui.widgets.braille_renderer import render_braille

WIDTH = 22
HEIGHT = 12

# Bee body with outlined hollow interior — edges define the shape,
# empty space inside gives it personality.
# Body only (without wings - wings are animated separately)
BODY_DOTS = [
    {5, 16},  # Row 0: Antennae tips
    {6, 7, 14, 15},  # Row 1: Antennae stems
    {7, 8, 9, 10, 11, 12, 13, 14},  # Row 2: Head top (solid)
    {7, 9, 12, 14},  # Row 3: Face outline + eyes (9, 12)
    {6, 7, 8, 9, 10, 11, 12, 13, 14, 15},  # Row 4: Thorax (solid, 10 wide)
    {6, 7, 14, 15},  # Row 5: Hollow interior (edges only)
    {6, 7, 8, 9, 10, 11, 12, 13, 14, 15},  # Row 6: Stripe (solid, 10 wide)
    {7, 14},  # Row 7: Hollow interior (edges only)
    {7, 8, 9, 10, 11, 12, 13, 14},  # Row 8: Abdomen (solid, 8 wide)
    {8, 13},  # Row 9: Outline edges
    {9, 10, 11, 12},  # Row 10: Taper
    {10, 11},  # Row 11: Stinger
]

# Starting position includes wings down
STARTING_DOTS = [
    {5, 16},  # Row 0: Antennae tips
    {6, 7, 14, 15},  # Row 1: Antennae stems
    {7, 8, 9, 10, 11, 12, 13, 14},  # Row 2: Head
    {7, 9, 12, 14},  # Row 3: Face + eyes
    {6, 7, 8, 9, 10, 11, 12, 13, 14, 15},  # Row 4: Thorax
    {
        1,
        2,
        3,
        4,
        5,
        6,
        7,
        14,
        15,
        16,
        17,
        18,
        19,
        20,
    },  # Row 5: Wings edge + hollow body
    {
        0,
        1,
        4,
        5,
        6,
        7,
        8,
        9,
        10,
        11,
        12,
        13,
        14,
        15,
        16,
        17,
        20,
        21,
    },  # Row 6: Wings outlined + stripe
    {1, 2, 3, 4, 5, 7, 14, 16, 17, 18, 19, 20},  # Row 7: Wings edge + hollow body
    {7, 8, 9, 10, 11, 12, 13, 14},  # Row 8: Abdomen
    {8, 13},  # Row 9: Outline
    {9, 10, 11, 12},  # Row 10: Taper
    {10, 11},  # Row 11: Stinger
]

# --- Wing positions: consistent outlined shape, shifted vertically ---
# Each position uses the same template:
#   solid edge (5 wide) / outlined middle (window cutout) / solid edge (5 wide)

# Wing template rows (reused across all positions)
_WING_EDGE = {1, 2, 3, 4, 5, 16, 17, 18, 19, 20}  # solid: 5 per side
_WING_MID = {0, 1, 4, 5, 16, 17, 20, 21}  # outlined: ends + window


def _make_wings(top_row: int) -> set[complex]:
    return (
        {1j * top_row + x for x in _WING_EDGE}
        | {1j * (top_row + 1) + x for x in _WING_MID}
        | {1j * (top_row + 2) + x for x in _WING_EDGE}
    )


# Position 0: Wings down (resting)
WINGS_DOWN = _make_wings(5)

# Position 1: Wings slightly raised
WINGS_MID_LOW = _make_wings(4)

# Position 2: Wings mid position
WINGS_MID_HIGH = _make_wings(3)

# Position 3: Wings up (highest)
WINGS_UP = _make_wings(2)

# Wing animation sequence: down -> mid-low -> mid-high -> up -> mid-high -> mid-low -> down
_WING_SEQUENCE = [
    WINGS_DOWN,
    WINGS_MID_LOW,
    WINGS_MID_HIGH,
    WINGS_UP,
    WINGS_MID_HIGH,
    WINGS_MID_LOW,
]

# --- Eye blink (eyes at row 3, columns 9 and 12) ---

BLINK_CLOSE = {"remove": {3j + 9, 3j + 12}, "add": set[complex]()}
BLINK_OPEN = {"remove": set[complex](), "add": {3j + 9, 3j + 12}}

# --- Antenna wiggle ---

ANTENNA_OUT = {"remove": {0j + 5, 0j + 16}, "add": {0j + 4, 0j + 17}}
ANTENNA_IN = {"remove": {0j + 4, 0j + 17}, "add": {0j + 5, 0j + 16}}

# Animation timing — randomised ranges for organic, non-repetitive feel.
_TICK_RATE = 0.12  # seconds per tick

_WING_FLAP_TICKS = 1  # 0.12s per wing position
_WING_REST_MIN = 2  # 0.24s minimum rest between flap cycles
_WING_REST_MAX = 10  # 1.20s maximum rest
_DOUBLE_FLAP_CHANCE = 0.25  # chance of skipping rest for an eager double-flap

_BLINK_HOLD = 2  # 0.24s eyes shut
_BLINK_MIN = 20  # 2.40s minimum between blinks
_BLINK_MAX = 50  # 6.00s maximum

_ANTENNA_HOLD = 6  # 0.72s antennae spread
_ANTENNA_MIN = 30  # 3.60s minimum between wiggles
_ANTENNA_MAX = 60  # 7.20s maximum

# Body dots (without wings) - used to reconstruct bee during wing animation
_BODY_DOTS = {1j * y + x for y, row in enumerate(BODY_DOTS) for x in row}


class Bee(Static):
    def __init__(self, animate: bool = True, **kwargs: Any) -> None:
        super().__init__(**kwargs, classes="banner-bee")
        self._dots = {1j * y + x for y, row in enumerate(STARTING_DOTS) for x in row}
        self._do_animate = animate
        self._freeze_requested = False
        self._timer: Timer | None = None

        # Wing animation state
        self._wing_pos = 0  # Current position in wing sequence
        self._wing_counter = 0  # Ticks since last wing change
        self._wing_resting = True  # Whether wings are in rest phase
        self._wing_rest_target = random.randint(_WING_REST_MIN, _WING_REST_MAX)

        # Eye blink state
        self._eyes_closed = False
        self._blink_counter = 0
        self._next_blink = random.randint(_BLINK_MIN, _BLINK_MAX)

        # Antenna wiggle state
        self._antennae_out = False
        self._antenna_counter = 0
        self._next_antenna = random.randint(_ANTENNA_MIN, _ANTENNA_MAX)

    def compose(self) -> ComposeResult:
        yield Static(render_braille(self._dots, WIDTH, HEIGHT), classes="bee-sprite")

    def on_mount(self) -> None:
        self._inner = self.query_one(".bee-sprite", Static)
        if self._do_animate:
            self._timer = self.set_interval(_TICK_RATE, self._tick)

    def freeze_animation(self) -> None:
        self._freeze_requested = True

    def _is_at_rest(self) -> bool:
        return (
            self._wing_resting
            and self._wing_pos == 0
            and not self._eyes_closed
            and not self._antennae_out
        )

    def _update_wings(self) -> bool:
        self._wing_counter += 1
        if self._wing_resting:
            if self._wing_counter < self._wing_rest_target:
                return False
            self._wing_resting = False
            self._wing_counter = 0
            return True

        if self._wing_counter < _WING_FLAP_TICKS:
            return False

        self._wing_pos = (self._wing_pos + 1) % len(_WING_SEQUENCE)
        self._wing_counter = 0
        if self._wing_pos == 0 and random.random() >= _DOUBLE_FLAP_CHANCE:
            self._wing_resting = True
            self._wing_rest_target = random.randint(_WING_REST_MIN, _WING_REST_MAX)
        return True

    def _update_blink(self) -> bool:
        self._blink_counter += 1
        if self._eyes_closed:
            if self._blink_counter < _BLINK_HOLD:
                return False
            self._apply(BLINK_OPEN)
            self._eyes_closed = False
            self._blink_counter = 0
            self._next_blink = random.randint(_BLINK_MIN, _BLINK_MAX)
            return True

        if self._blink_counter < self._next_blink:
            return False
        self._apply(BLINK_CLOSE)
        self._eyes_closed = True
        self._blink_counter = 0
        return True

    def _update_antenna(self) -> bool:
        self._antenna_counter += 1
        if self._antennae_out:
            if self._antenna_counter < _ANTENNA_HOLD:
                return False
            self._apply(ANTENNA_IN)
            self._antennae_out = False
            self._antenna_counter = 0
            self._next_antenna = random.randint(_ANTENNA_MIN, _ANTENNA_MAX)
            return True

        if self._antenna_counter < self._next_antenna:
            return False
        self._apply(ANTENNA_OUT)
        self._antennae_out = True
        self._antenna_counter = 0
        return True

    def _rebuild_current_frame(self) -> None:
        # Reconstruct bee: body + current wing position + eye/antenna modifications.
        self._dots = _BODY_DOTS | _WING_SEQUENCE[self._wing_pos]
        if self._eyes_closed:
            self._dots -= BLINK_CLOSE["remove"]
            self._dots |= BLINK_CLOSE["add"]
        if self._antennae_out:
            self._dots -= ANTENNA_OUT["remove"]
            self._dots |= ANTENNA_OUT["add"]
        self._inner.update(render_braille(self._dots, WIDTH, HEIGHT))

    def _tick(self) -> None:
        if self._freeze_requested and self._is_at_rest():
            if self._timer:
                self._timer.stop()
            self._timer = None
            return

        changed = any((
            self._update_wings(),
            self._update_blink(),
            self._update_antenna(),
        ))
        if changed:
            self._rebuild_current_frame()

    def _apply(self, transition: dict[str, set[complex]]) -> None:
        self._dots -= transition["remove"]
        self._dots |= transition["add"]
