import reflex as rx

from ai_analsyis_flow_people.utils.styles import FONT_FAMILY


def sidebar_link(text: str, href: str, icon: str):
    return rx.link(
        rx.flex(
            rx.icon_button(
                rx.icon(tag=icon, weight=16, height=16),
                variant="soft",
            ),
            text,
            class_name="sidebar_link_button",
            py="2",
            px="4",
            spacing="3"
        ),
        href=href,
        class_name="sidebar_link"
    )


def sidebar(
    *sidebar_links,
    **props,
) -> rx.Component:
    logo_src = props.get("logo_src", "/logo.png")
    heading = props.get("heading", "NOT SET")
    return rx.vstack(
        rx.hstack(
            rx.image(src=logo_src, height="28px", border_radius="8px"),
            rx.heading(
                heading,
                id="sidebar_header"
            ),
            id="sidebar_vstack_header"
        ),
        rx.divider(margin_y="3"),
        rx.vstack(
            *sidebar_links,
            id="sidebar_vstack_links"
        ),
        id="sidebar"
    )


dashboard_sidebar = sidebar(
    sidebar_link(text="Home", href="/", icon="home"),
    sidebar_link(text="Live Camera", href="/camera", icon="camera"),
    sidebar_link(text="Chaty", href="/chaty", icon="message-square"),
    sidebar_link(text="Azure", href="/azure", icon="database"),
    sidebar_link(text="AI Results Notebooks", href="/notebooks", icon="notebook"),
    sidebar_link(text="Dashboard RabbitMQ", href="/rabbitmq", icon="layout-dashboard"),
    sidebar_link(text="Dashboard BigData", href="/bigdata", icon="layout-dashboard"),
    sidebar_link(text="Documentation", href="/documentation", icon="book-check"),
    sidebar_link(text="Conclusions", href="/conclusions", icon="list-end"),
    logo_src="/favicon.ico",
    heading="Project AI",
)


class State(rx.State):
    pass


def navbar(heading: str, childs=None) -> rx.Component:
    if childs is None:
        childs = ''

    return rx.hstack(
        rx.heading(heading, font_family=FONT_FAMILY, size="7"),
        rx.spacer(),
        childs,
        id="navbar"
    )
