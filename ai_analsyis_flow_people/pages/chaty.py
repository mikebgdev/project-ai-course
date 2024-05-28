import reflex as rx

from ai_analsyis_flow_people.components.template import template
from ai_analsyis_flow_people.components.chat import chat
from ai_analsyis_flow_people.components.chat.navbar import navbar


@template
def chaty() -> rx.Component:
    return rx.box(
        navbar(),
        rx.vstack(
            chat.chat(),
            chat.action_bar(),
            background_color=rx.color("mauve", 2),
            color=rx.color("mauve", 12),
            min_height="100vh",
            align_items="stretch",
            spacing="0",
        ),
        class_name="page"
    )
