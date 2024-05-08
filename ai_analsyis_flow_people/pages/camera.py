import reflex as rx

from ai_analsyis_flow_people.navigation import navbar
from ai_analsyis_flow_people.template import template

@template
def camera() -> rx.Component:
    return rx.box(
            navbar(heading="Live Camera"),
            rx.box(
                rx.text("placeholder"),
                margin_top="calc(50px + 2em)",
                padding="2em",
            ),
            padding_left="250px",
        )
