import reflex as rx

from ai_analsyis_flow_people.components.navigation import navbar
from ai_analsyis_flow_people.components.template import template
from ai_analsyis_flow_people.components.graphs import stat_card
from ai_analsyis_flow_people.consumers.rabbit_consumer import DashboardRabbitMqState


def prepare_data_stat_card():
    return [
        [
            "Queues",
            DashboardRabbitMqState.queues
        ],
        [
            "Consumers",
            DashboardRabbitMqState.consumers
        ],
        [
            "Connections",
            DashboardRabbitMqState.connections
        ],
        [
            "Channels",
            DashboardRabbitMqState.channels
        ],
        [
            "Incoming messages",
            DashboardRabbitMqState.incoming_messages
        ],
        [
            "Outgoing messages",
            DashboardRabbitMqState.outgoing_messages
        ],
        [
            "Ready messages",
            DashboardRabbitMqState.ready_messages
        ],
        [
            "Unacknowledged messages",
            DashboardRabbitMqState.unacknowledged_messages
        ]
    ]


def content_grid():
    return rx.chakra.grid(
        *[
            rx.chakra.grid_item(stat_card(*c), col_span=1, row_span=1)
            for c in prepare_data_stat_card()
        ],
        template_columns="repeat(4, 1fr)",
        width="100%",
        gap=4,
        row_gap=8,
    )


@template
def rabbitmq() -> rx.Component:
    return rx.box(
        navbar(heading="Dashboard RabbitMq"),
        rx.box(
            content_grid(),
            padding="2em",
            min_height="calc(100vh - calc(50px + 2em))",
            background_color=rx.color("mauve", 2),
        ),
        padding_top="calc(50px + 2em)",
        padding_left="250px",
        on_mount=DashboardRabbitMqState.update_metrics,
    )
