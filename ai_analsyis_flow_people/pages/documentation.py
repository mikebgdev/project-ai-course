import reflex as rx

from ai_analsyis_flow_people.components.navigation import navbar
from ai_analsyis_flow_people.components.template import template


@template
def documentation() -> rx.Component:
    return rx.box(
        navbar(heading="Documentation"),
        rx.box(
            rx.text("placeholder"),
            background_color=rx.color("mauve", 2),
            padding="2em",
            min_height="calc(100vh - calc(50px + 2em))",
        ),
        padding_top="calc(50px + 2em)",
        padding_left="250px",
    )
