import reflex as rx

from ai_analsyis_flow_people.utils.styles import THEME, STYLESHEETS, STYLE

from ai_analsyis_flow_people.pages.index import index
from ai_analsyis_flow_people.pages.camera import camera
from ai_analsyis_flow_people.pages.chaty import chaty
from ai_analsyis_flow_people.pages.notebooks import notebooks
from ai_analsyis_flow_people.pages.rabbitmq import rabbitmq
from ai_analsyis_flow_people.pages.bigdata import bigdata
from ai_analsyis_flow_people.pages.documentation import documentation
from ai_analsyis_flow_people.pages.conclusions import conclusions
from ai_analsyis_flow_people.pages.azure import azure

app = rx.App(
    theme=THEME,
    stylesheets=STYLESHEETS,
    style=STYLE
)

app.add_page(index, route="/")
app.add_page(camera, route="/camera")
app.add_page(chaty, route="/chaty")
app.add_page(notebooks, route="/notebooks")
app.add_page(rabbitmq, route="/rabbitmq")
app.add_page(bigdata, route="/bigdata")
app.add_page(documentation, route="/documentation")
app.add_page(conclusions, route="/conclusions")
app.add_page(azure, route="/azure")
