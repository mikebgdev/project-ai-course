import reflex as rx

from ai_analsyis_flow_people.components.navigation import navbar
from ai_analsyis_flow_people.components.template import template
from ai_analsyis_flow_people.utils.constants import DOC_CONCLUSION
from ai_analsyis_flow_people.utils.markdown import markdown_component


@template
def conclusions() -> rx.Component:
    return rx.box(
        navbar(heading="Conclusion"),
        rx.box(
            markdown_component(DOC_CONCLUSION),
            class_name="content"
        ),
        class_name="page"
    )
