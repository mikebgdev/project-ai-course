import reflex as rx


def card(*children, **props):
    return rx.card(
        *children,
        box_shadow="rgba(0, 0, 0, 0.1) 0px 4px 6px -1px, rgba(0, 0, 0, 0.06) 0px 2px 4px -1px;",
        **props,
    )


def stat_card(title: str, stat) -> rx.Component:
    return card(
        rx.hstack(
            rx.vstack(
                rx.heading(title),
                rx.text(stat)
            ),
        ),
    )
