import reflex as rx

from ai_analsyis_flow_people.navigation import navbar
from ai_analsyis_flow_people.template import template
# from ai_analsyis_flow_people.constants import blur_ratio, model_face, live_video_url

import subprocess

websocket_process = None



def start_detection():
    global websocket_process

    if not is_websocket_running():
        websocket_process = subprocess.Popen(['python', 'ai_analsyis_flow_people/utils/websocket_server.py'])
        return rx.console_log("Detección iniciada")
    else:
        return rx.console_log("El WebSocket ya está iniciado")


def stop_detection():
    global websocket_process

    if is_websocket_running():
        websocket_process.terminate()
        websocket_process.wait()
        return rx.console_log("Detección detenida")
    else:
        return rx.console_log("El WebSocket no está iniciado")


def is_websocket_running():
    global websocket_process

    return websocket_process is not None and websocket_process.poll() is None


class ExternalJSState(rx.State):
    @rx.background
    async def call_external_js(self, fuction):
        return rx.call_script(fuction)

@template
def camera() -> rx.Component:
    return rx.box(
        navbar(heading="Live Camera"),
        rx.box(
            rx.hstack(
                rx.button("Start WebScoket", on_click=start_detection),
                rx.button("Start Detection", on_click=ExternalJSState.call_external_js("start_detection()")),
                # rx.button("Start Detection", id="start", on_click=start_detection),
                rx.button("Stop Detection", on_click=stop_detection),
            ),
            rx.container(
                rx.image(id="video", width="640", height="480"),
                id="video-feed",

            ),
            rx.script(src="/static/video_script.js"),
            margin_top="calc(50px + 2em)",
            padding="2em",
        ),
        padding_left="250px",
        # height="100vh"
    )
