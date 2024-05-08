"""The main Dashboard App."""

from rxconfig import config

import reflex as rx

from ai_analsyis_flow_people.styles import BACKGROUND_COLOR, FONT_FAMILY, THEME, STYLESHEETS

from ai_analsyis_flow_people.pages.index import index
from ai_analsyis_flow_people.pages.camera import camera
from ai_analsyis_flow_people.pages.chaty import chaty
from ai_analsyis_flow_people.pages.notebooks import notebooks
from ai_analsyis_flow_people.pages.rabbitmq import rabbitmq
from ai_analsyis_flow_people.pages.bigdata import bigdata
from ai_analsyis_flow_people.pages.documentation import documentation

# Create app instance and add index page.
app = rx.App(
    theme=THEME,
    stylesheets=STYLESHEETS,
    # heigth="100vh"
)

app.add_page(index, route="/")
app.add_page(camera, route="/camera")
app.add_page(chaty, route="/chaty")
app.add_page(notebooks, route="/notebooks")
app.add_page(rabbitmq, route="/rabbitmq")
app.add_page(bigdata, route="/bigdata")
app.add_page(documentation, route="/documentation")
