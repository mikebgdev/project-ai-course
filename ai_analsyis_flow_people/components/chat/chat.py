import reflex as rx

from ai_analsyis_flow_people.components.chat.chat_state import QA, ChatState
from ai_analsyis_flow_people.components.chat.loading_icon import loading_icon

message_style = dict(display="inline-block", padding="1em", border_radius="8px", max_width=["30em", "30em", "50em", "50em", "50em", "50em"])


def message(qa: QA) -> rx.Component:
    return rx.box(
        rx.box(
            rx.markdown(
                qa.question,
                background_color=rx.color("mauve", 4),
                color=rx.color("mauve", 12),
                **message_style,
            ),
            text_align="right",
            margin_top="1em",
        ),
        rx.box(
            rx.markdown(
                qa.answer,
                background_color=rx.color("accent", 4),
                color=rx.color("accent", 12),
                **message_style,
            ),
            text_align="left",
            padding_top="1em",
        ),
        width="100%",
    )


def chat() -> rx.Component:
    """List all the messages in a single conversation."""
    return rx.vstack(
        rx.box(rx.foreach(ChatState.chats[ChatState.current_chat], message), width="100%"),
        py="8",
        flex="1",
        width="100%",
        max_width="50em",
        padding_x="4px",
        align_self="center",
        overflow="hidden",
        padding_bottom="5em",
    )


def action_bar() -> rx.Component:
    return rx.center(
        rx.vstack(
            rx.chakra.form(
                rx.chakra.form_control(
                    rx.hstack(
                        rx.radix.text_field.root(
                            rx.radix.text_field.input(
                                placeholder="Type something...",
                                id="question",
                                width=["15em", "20em", "45em", "50em", "50em", "50em"],
                            ),
                            rx.radix.text_field.slot(
                                rx.tooltip(
                                    rx.icon("info", size=18),
                                    content="Enter a question to get a response.",
                                )
                            ),
                        ),
                        rx.button(
                            rx.cond(
                                ChatState.processing,
                                loading_icon(height="1em"),
                                rx.text("Send"),
                            ),
                            type="submit",
                        ),
                        align_items="center",
                    ),
                    is_disabled=ChatState.processing,
                ),
                on_submit=ChatState.process_question,
                reset_on_submit=True,
            ),
            align_items="center",
        ),
        position="sticky",
        bottom="0",
        left="0",
        padding_y="16px",
        backdrop_filter="auto",
        backdrop_blur="lg",
        border_top=f"1px solid {rx.color('mauve', 3)}",
        background_color=rx.color("accent", 2),
        align_items="stretch",
        width="100%",
    )
