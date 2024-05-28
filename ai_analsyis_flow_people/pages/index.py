import reflex as rx

from ai_analsyis_flow_people.components.navigation import navbar
from ai_analsyis_flow_people.components.template import template
from ai_analsyis_flow_people.utils.constants import DOC_INDEX
from ai_analsyis_flow_people.utils.markdown import markdown_component


@template
def index() -> rx.Component:
    return rx.box(
        navbar(heading="Flujo de Análisis de IA para el Seguimiento de Personas"),
        rx.box(
            markdown_component(DOC_INDEX),
            class_name="content"
        ),
        class_name="page"
    )
