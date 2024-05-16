import reflex as rx
from ai_analsyis_flow_people.components.navigation import navbar
from ai_analsyis_flow_people.components.template import template
import sys
import subprocess
import psutil

# class WebsocketState():
websocket_process = None


def start_websocket():
    global websocket_process

    # Verificar si hay un proceso websocket en ejecución y, si es así, terminarlo
    for proc in psutil.process_iter(['pid', 'name']):
        if proc.info['name'] == 'python' and 'websocket_server.py' in ' '.join(proc.cmdline()):
            proc.terminate()
            proc.wait()

    python_executable = sys.executable
    script_path = 'yolov8/websocket_server.py'

    # Iniciar el proceso websocket
    websocket_process = subprocess.Popen([python_executable, script_path], stdout=subprocess.PIPE,
                                         stderr=subprocess.PIPE)
    stdout, stderr = websocket_process.communicate()
    return rx.console_log(f"WebSocket STDERR: {stderr.decode('utf-8')}")

# def start_websocket():
#     global websocket_process
#
#     # if not is_websocket_running():
#     python_executable = sys.executable
#     script_path = 'yolov8/websocket_server.py'
#     # try:
#     websocket_process = subprocess.Popen([python_executable, script_path], stdout=subprocess.PIPE,
#                                          stderr=subprocess.PIPE)
#     stdout, stderr = websocket_process.communicate()
#     # return rx.console_log(f"WebSocket STDOUT: {stdout.decode('utf-8')}")
#     return rx.console_log(f"WebSocket STDERR: {stderr.decode('utf-8')}")
#     # return rx.console_log("Websocket iniciado")
#     # except Exception as e:
#     #     return rx.console_log(f"Error al iniciar WebSocket: {e}")
#     # else:
#     #     return rx.console_log("El WebSocket ya está iniciado")

def stop_websocket():
    global websocket_process

    if websocket_process is not None:
        websocket_process.terminate()
        websocket_process.wait()
        websocket_process = None
        return rx.console_log("Websocket detenido")
    else:
        return rx.console_log("El WebSocket no está iniciado")

# def stop_websocket():
#     global websocket_process
#
#     # if is_websocket_running():
#     websocket_process.terminate()
#     websocket_process.wait()
#     websocket_process = None
#     return rx.console_log("Websocket detenido")
#     # else:
#     #     return rx.console_log("El WebSocket no está iniciado")


def is_websocket_running():
    global websocket_process

    return websocket_process is not None and websocket_process.poll() is None


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
                rx.button("Start WebSocket", on_click=start_websocket),
                rx.button("Stop WebSocket", on_click=stop_websocket),
                rx.button("Start Detection", on_click=ExternalJSState.call_external_js("start_detection()")),
                rx.button("Stop Detection", on_click=stop_websocket),  # Corregido aquí
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
