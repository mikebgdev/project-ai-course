import reflex as rx

from ai_analsyis_flow_people.navigation import navbar
from ai_analsyis_flow_people.template import template

@template
def bigdata() -> rx.Component:
    return rx.box(
            navbar(heading="Dashboard Big Data"),
            rx.box(
                rx.text("placeholder"),
                margin_top="calc(50px + 2em)",
                padding="2em",
            ),
            padding_left="250px",
        )
