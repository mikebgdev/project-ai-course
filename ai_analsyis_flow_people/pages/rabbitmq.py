import reflex as rx

from ai_analsyis_flow_people.components.navigation import navbar
from ai_analsyis_flow_people.components.template import template
from ai_analsyis_flow_people.components.graphs import stat_card
from ai_analsyis_flow_people.consumers.rabbit_consumer import DashboardRabbitMqState, prepare_data_stat_card


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
            class_name="content"
        ),
        class_name="page",
        on_mount=DashboardRabbitMqState.update_metrics,
    )
