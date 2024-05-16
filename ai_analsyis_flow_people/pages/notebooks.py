import reflex as rx

from ai_analsyis_flow_people.components.navigation import navbar
from ai_analsyis_flow_people.components.template import template


@template
def notebooks() -> rx.Component:
    return rx.box(
        navbar(heading="Notebooks"),
        rx.box(
            rx.text("placeholder"),
            margin_top="calc(50px + 2em)",
            padding="2em",
        ),
        padding_left="250px",
    )
