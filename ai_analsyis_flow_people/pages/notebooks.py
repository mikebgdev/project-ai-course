import reflex as rx

from ai_analsyis_flow_people.components.navigation import navbar
from ai_analsyis_flow_people.components.template import template


def content():
    return rx.box(
        rx.section(
            rx.heading("Análisis Exploratorio de Datos (EDA)", level=1),
            rx.hstack(
                rx.image(src="/img/modelos/distribucion_cordx.png", alt="Distribución Cord X", width="auto",
                         max_width="30%"),
                rx.image(src="/img/modelos/distribucion_cordy.png", alt="Distribución Cord Y", width="auto",
                         max_width="30%"),
                rx.image(src="/img/modelos/relacion_cord.png", alt="Relación Cord XY", width="auto", max_width="30%"),
                spacing="2",
            )
        ),
        rx.section(
            rx.heading(
                "Clustering: Identificar patrones de agrupación en el flujo peatonal para mejorar la planificación urbana.",
                level=1),
            rx.section(
                rx.heading("K-Means Clustering", level=2),
                rx.hstack(
                    rx.image(src="/img/modelos/elbow.png", alt="Elbow Method K-Means", width="auto", max_width="50%"),
                    rx.image(src="/img/modelos/kmeans.png", alt="K-Means Clustering", width="auto", max_width="50%"),
                    spacing="2",
                ),
                rx.text("Silhouette Score para K-Means: 0.5872")
            ),
            rx.section(
                rx.heading("DBSCAN Clustering", level=2),
                rx.hstack(
                    rx.image(src="/img/modelos/dbscan.png", alt="DBSCAN Clustering", width="auto", max_width="50%"),
                    spacing="2",
                ),
                rx.text("Silhouette Score para DBSCAN: 0.6451")
            )
        ),
        rx.section(
            rx.heading(
                "Classification: Identificar diferentes categorías de comportamiento en el flujo peatonal para mejorar la segmentación y el análisis.",
                level=1),
            rx.section(
                rx.heading("Árbol de Decisión", level=2),
                rx.hstack(
                    rx.image(src="/img/modelos/decision_tree.png", alt="Decision tree", width="auto", max_width="100%"),
                    spacing="2",
                ),
                rx.text("Accuracy del Árbol de Decisión: 0.90")
            ),
            rx.section(
                rx.heading("Random Forest", level=2),
                rx.hstack(
                    rx.image(src="/img/modelos/random_forest.png", alt="Random Forest", width="auto", max_width="50%"),
                    spacing="2",
                ),
                rx.text("Accuracy del Bosque Aleatorio: 0.95")
            ),
        ),
        rx.section(
            rx.heading(
                "Regresión: Predecir valores continuos relacionados con el flujo peatonal para mejorar la planificación y gestión urbana.",
                level=1),
            rx.section(
                rx.heading("Regresión Lineal", level=2),
                rx.hstack(
                    rx.image(src="/img/modelos/regresion_linea.png", alt="Regression Linea", width="auto",
                             max_width="100%"),
                    spacing="2",
                )
            ),
            rx.section(
                rx.heading("Regresión Polinómica", level=2),
                rx.hstack(
                    rx.image(src="/img/modelos/regresion_poly.png", alt="Regression Ploy", width="auto",
                             max_width="50%"),
                    spacing="2",
                )
            ),
            rx.section(
                rx.heading("Results", level=2),
                rx.vstack(
                    rx.image(src="/img/modelos/regresion_r2.png", alt="Regression R2", width="auto", max_width="50%"),
                    rx.image(src="/img/modelos/regresion_mse.png", alt="Regression MS2", width="auto", max_width="50%"),
                    spacing="2",
                )
            ),
        ),
        rx.section(
            rx.heading("Análisis de resultados", level=1),
            rx.text(
                "De todos los modelos realizados y con los datos disponibles, el único que resulta útil por el "
                "momento es el de clustering. Este modelo nos permite identificar dónde se agrupa la gente, "
                "facilitando así el análisis de patrones de comportamiento.")
        ),
        class_name="content"
    )


@template
def notebooks() -> rx.Component:
    return rx.box(
        navbar(heading="Resultados de los Modelos"),
        content(),
        class_name="page"
    )
