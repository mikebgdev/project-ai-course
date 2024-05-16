import reflex as rx

from ai_analsyis_flow_people.navigation import navbar
from ai_analsyis_flow_people.template import template

import subprocess

websocket_process = None

from pathlib import Path

def start_websocket(): # TODO REVISAR
    global websocket_process

    if not is_websocket_running():
        websocket_process = subprocess.Popen(['python','yolov8/websocket_server.py'])
        return rx.console_log("Websocket iniciado")
    else:
        return rx.console_log("El WebSocket ya está iniciado")


def stop_websocket():# TODO REVISAR
    global websocket_process

    if is_websocket_running():
        websocket_process.terminate()
        websocket_process.wait()
        return rx.console_log("Websocket detenido")
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
                rx.button("Start WebScoket", on_click=start_websocket),
                rx.button("Stop WebScoket", on_click=stop_websocket),
                rx.button("Start Detection", on_click=ExternalJSState.call_external_js("start_detection()")),
                rx.button("Stop Detection", on_click=stop_websocket),
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
