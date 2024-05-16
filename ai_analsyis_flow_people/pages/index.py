import reflex as rx

from ai_analsyis_flow_people.components.navigation import navbar
from ai_analsyis_flow_people.components.template import template


def content_grid():
    return rx.vstack(
        rx.heading("Flujo de Análisis de IA para el Seguimiento de Personas"),
        rx.text(
            "El proyecto utiliza YOLOv8 para reconocer personas en imágenes en tiempo real. Además de reconocer "
            "personas, el modelo también guarda el recorrido de cada individuo y predice su movimiento futuro. Para "
            "proteger la privacidad de las personas, se utiliza YOLOv8-face para difuminar automáticamente las caras "
            "detectadas en las imágenes."),
        rx.text(
            "Los datos generados por el reconocimiento de personas se almacenan en una base de datos MongoDB. Para "
            "gestionar eficientemente la transferencia de datos entre el sistema de reconocimiento y la base de "
            "datos, el proyecto hace uso de las colas de RabbitMQ. Las solicitudes de almacenamiento de datos se "
            "encolan en RabbitMQ y luego son procesadas por Apache NiFi, que lee las colas de RabbitMQ y guarda los "
            "datos en MongoDB. Además de guardar los datos en la base de datos, NiFi genera un archivo CSV y un "
            "archivo JSON para su análisis posterior."),
        rx.text(
            "Además, el proyecto cuenta con dos dashboards para monitorear el rendimiento y las métricas tanto de "
            "RabbitMQ como de MongoDB. Estos dashboards proporcionan una visión instantánea del estado de los "
            "sistemas de mensajería y bases de datos, permitiendo una gestión más eficiente y efectiva de los "
            "recursos.")
    )


@template
def index() -> rx.Component:
    return rx.box(
        navbar(heading="AI & Big Data Project"),
        rx.box(
            content_grid(),
            margin_top="calc(50px + 2em)",
            padding="2em",
        ),
        padding_left="250px",
    )
