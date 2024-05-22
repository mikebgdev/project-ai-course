import reflex as rx

from ai_analsyis_flow_people.components.navigation import navbar
from ai_analsyis_flow_people.components.template import template


def content():
    return rx.box(
        rx.section(
            rx.heading("Análisis Exploratorio de Datos (EDA)", level=1),
            rx.hstack(
                rx.image(src="/img/modelos/distribucion_cordx.png", alt="Distribución Cord X", width="auto", max_width="30%"),
                rx.image(src="/img/modelos/distribucion_cordy.png", alt="Distribución Cord Y", width="auto", max_width="30%"),
                rx.image(src="/img/modelos/relacion_cord.png", alt="Relación Cord XY", width="auto", max_width="30%"),
                spacing="2",
            ),
            margin_bottom="2em",
        ),
        rx.section(
            rx.heading("Clustering", level=1),
            rx.section(
                rx.heading("K-Means Clustering", level=2),
                rx.hstack(
                    rx.image(src="/img/modelos/elbow.png", alt="Elbow Method K-Means", width="auto", max_width="50%"),
                    rx.image(src="/img/modelos/kmeans.png", alt="K-Means Clustering", width="auto", max_width="50%"),
                    spacing="2",
                ),
                rx.text("Silhouette Score para K-Means: 0.5872"),
                margin_bottom="2em",
            ),
            rx.section(
                rx.heading("DBSCAN Clustering", level=2),
                rx.hstack(
                    rx.image(src="/img/modelos/dbscan.png", alt="DBSCAN Clustering", width="auto", max_width="50%"),
                    spacing="2",
                ),
                rx.text("Silhouette Score para DBSCAN: 0.6451"),
                margin_bottom="2em",
            ),
        ),
        rx.section(
            rx.heading("Classification", level=1),
            rx.section(
                rx.heading("Árbol de Decisión", level=2),
                rx.hstack(
                    rx.image(src="/img/modelos/decision_tree.png", alt="Decision tree", width="auto", max_width="100%"),
                    spacing="2",
                ),
                rx.text("Accuracy del Árbol de Decisión: 0.90"),
                margin_bottom="2em",
            ),
            rx.section(
                rx.heading("Random Forest", level=2),
                rx.hstack(
                    rx.image(src="/img/modelos/random_forest.png", alt="Random Forest", width="auto", max_width="50%"),
                    spacing="2",
                ),
                rx.text("Accuracy del Bosque Aleatorio: 0.95"),
                margin_bottom="2em",
            ),
        ),
        background_color=rx.color("mauve", 2),
        padding="2em",
        min_height="calc(100vh - 50px - 2em)",
    )


@template
def notebooks() -> rx.Component:
    return rx.box(
        navbar(heading="Resultados de los Modelos"),
        content(),
        padding_top="calc(50px + 2em)",
        padding_left="250px",
    )
