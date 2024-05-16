import reflex as rx
from ai_analsyis_flow_people.components.navigation import navbar
from ai_analsyis_flow_people.components.template import template


class ExternalJSState(rx.State):
    @rx.background
    async def call_external_js(self, function):
        return rx.call_script(function)


@template
def camera() -> rx.Component:
    return rx.box(
        navbar(heading="Live Camera"),
        rx.box(
            rx.hstack(
                rx.button("Start Detection", on_click=ExternalJSState.call_external_js("start_detection()")),
                # rx.button("Stop Detection", on_click=Websocket.stop_websocket()),  # Corregido aquí
            ),
            rx.container(
                rx.image(id="video", width="640", height="480"),
                rx.box(id="persons"),
                id="video-feed",
                padding_top="2em",
                padding_bot="2em"
            ),
            rx.script(src="/static/video_script.js"),
            margin_top="calc(50px + 2em)",
            padding="2em",
        ),
        padding_left="250px",
        # height="100vh"
    )
