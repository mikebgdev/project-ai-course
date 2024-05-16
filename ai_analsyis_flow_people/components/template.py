from typing import Callable

import reflex as rx

from ai_analsyis_flow_people.components.navigation import dashboard_sidebar
from ai_analsyis_flow_people.components.styles import BACKGROUND_COLOR, FONT_FAMILY


def template(page: Callable[[], rx.Component]) -> rx.Component:
    return rx.box(
        dashboard_sidebar,
        page(),
        background_color=BACKGROUND_COLOR,
        font_family=FONT_FAMILY,
    )
