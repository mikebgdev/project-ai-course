import reflex as rx
from reflex.components import lucide

from ai_analsyis_flow_people.styles import FONT_FAMILY


def sidebar_link(text: str, href: str, icon: str):
    return rx.link(
        rx.flex(
            rx.icon_button(
                rx.icon(tag=icon, weight=16, height=16),
                variant="soft",
            ),
            text,
            py="2",
            px="4",
            spacing="3",
            align="center",
            direction="row",
            font_family=FONT_FAMILY,
        ),
        href=href,
        width="100%",
        border_radius="8px",
        _hover={
            "background": "rgba(255, 255, 255, 0.1)",
            "backdrop_filter": "blur(10px)",
        },
    )


def sidebar(
    *sidebar_links,
    **props,
) -> rx.Component:
    logo_src = props.get("logo_src", "/logo.jpg")
    heading = props.get("heading", "NOT SET")
    return rx.vstack(
        rx.hstack(
            rx.image(src=logo_src, height="28px", border_radius="8px"),
            rx.heading(
                heading,
                font_family=FONT_FAMILY,
                size="5",
            ),
            width="100%",
            spacing="7",
        ),
        rx.divider(margin_y="3"),
        rx.vstack(
            *sidebar_links,
            padding_y="1em",
        ),
        width="250px",
        position="fixed",
        height="100%",
        left="0px",
        top="0px",
        align_items="left",
        z_index="10",
        backdrop_filter="blur(10px)",
        padding="1em",
    )


dashboard_sidebar = sidebar(
    sidebar_link(text="Home", href="/", icon="home"),
    sidebar_link(text="Live Camera", href="/camera", icon="camera"),
    sidebar_link(text="Chaty", href="/chaty", icon="message-square"),
    sidebar_link(text="AI Results Notebooks", href="/notebooks", icon="notebook"),
    sidebar_link(text="Dashboard RabbitMQ", href="/rabbitmq", icon="layout-dashboard"),
    sidebar_link(text="Dashboard BigData", href="/bigdata", icon="layout-dashboard"),
    sidebar_link(text="Documentation", href="/documentation", icon="book-check"),
    logo_src="/favicon.ico",
    heading="AI Project",
)


class State(rx.State):
    pass


def navbar(heading: str) -> rx.Component:
    return rx.hstack(
        rx.heading(heading, font_family=FONT_FAMILY, size="7"),
        rx.spacer(),
        position="fixed",
        width="calc(100% - 250px)",
        top="0px",
        z_index="1000",
        padding_x="2em",
        padding_top="2em",
        padding_bottom="1em",
        backdrop_filter="blur(10px)",
    )
