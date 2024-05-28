import reflex as rx

from ai_analsyis_flow_people.components.chat.chat_state import ChatState


def sidebar_chat(chat: str) -> rx.Component:
    """A sidebar chat item.

    Args:
        chat: The chat item.
    """
    return rx.drawer.close(rx.hstack(
        rx.button(
            chat, on_click=lambda: ChatState.set_chat(chat), width="80%", variant="surface"
        ),
        rx.button(
            rx.icon(
                tag="trash",
                on_click=ChatState.delete_chat,
                stroke_width=1,
            ),
            width="20%",
            variant="surface",
            color_scheme="red",
        ),
        width="100%",
    ))


def sidebar(trigger) -> rx.Component:
    """The sidebar component."""
    return rx.drawer.root(
        rx.drawer.trigger(trigger),
        rx.drawer.overlay(),
        rx.drawer.portal(
            rx.drawer.content(
                rx.vstack(
                    rx.heading("Chats", color=rx.color("mauve", 11)),
                    rx.divider(),
                    rx.foreach(ChatState.chat_titles, lambda chat: sidebar_chat(chat)),
                    align_items="stretch",
                    width="100%",
                ),
                top="auto",
                right="auto",
                height="100%",
                width="20em",
                padding="2em",
                background_color=rx.color("mauve", 2),
                outline="none",
            )
        ),
        direction="left",
    )


def modal(trigger) -> rx.Component:
    """A modal to create a new chat."""
    return rx.dialog.root(
        rx.dialog.trigger(trigger),
        rx.dialog.content(
            rx.hstack(
                rx.input(
                    placeholder="Type something...",
                    on_blur=ChatState.set_new_chat_name,
                    width=["15em", "20em", "30em", "30em", "30em", "30em"],
                ),
                rx.dialog.close(
                    rx.button(
                        "Create chat",
                        on_click=ChatState.create_chat,
                    ),
                ),
                background_color=rx.color("mauve", 1),
                spacing="2",
                width="100%",
            ),
        ),
    )


def navbar_old():
    return rx.box(
        rx.hstack(
            rx.hstack(
                rx.heading("Chat Arch btw"),
                align_items="center",
            ),
            rx.hstack(
                modal(rx.button("+ New chat")),
                sidebar(
                    rx.button(
                        rx.icon(
                            tag="messages-square",
                            color=rx.color("mauve", 12),
                        ),
                        background_color=rx.color("mauve", 6),
                    )
                ),
                align_items="center",
            ),
            justify_content="space-between",
            align_items="center",
        ),
        backdrop_filter="blur(10px)",
        backdrop_blur="lg",
        padding_x="2em",
        padding_top="2em",
        padding_bottom="1em",
        border_bottom=f"1px solid {rx.color('mauve', 3)}",
        background_color=rx.color("accent", 2),
        position="sticky",
        top="0",
        z_index="1000",
        align_items="center",
    )


def navbar():
    return rx.hstack(
        rx.heading("Chat Arch btw"),
        rx.spacer(),
        modal(rx.button("+ New chat")),
        sidebar(
            rx.button(
                rx.icon(
                    tag="messages-square",
                    color=rx.color("mauve", 12),
                ),
                background_color=rx.color("mauve", 6),
            )
        ),
        id="navbar"
    )
