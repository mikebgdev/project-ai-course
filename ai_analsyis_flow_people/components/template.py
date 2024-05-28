from typing import Callable

import reflex as rx

from ai_analsyis_flow_people.components.navigation import dashboard_sidebar
from ai_analsyis_flow_people.utils.styles import BACKGROUND_COLOR, FONT_FAMILY


def template(page: Callable[[], rx.Component]) -> rx.Component:
    return rx.box(
        dashboard_sidebar,
        page(),
        id="body",
    )
