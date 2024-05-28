import reflex as rx
from reflex.components.radix import themes as th

THEME = th.theme(
    appearance="dark",
    has_background=True,
    radius="large",
    accent_color="iris",
    scaling="100%",
    panel_background="solid",
)

STYLESHEETS = ["https://fonts.googleapis.com/css2?family=Share+Tech+Mono&display=swap"]

FONT_FAMILY = "Share Tech Mono"
BACKGROUND_COLOR = "var(--accent-2)"

STYLE = {
    "#body": {
        "background_color": BACKGROUND_COLOR,
        "font_family": FONT_FAMILY,
    },
    ".page": {
        "padding_top": "calc(50px + 2em)",
        "padding_left": "250px"
    },
    "#navbar": {
        "position": "fixed",
        "width": "calc(100% - 250px)",
        "top": "0px",
        "z_index": "1000",
        "padding_x": "2em",
        "padding_top": "2em",
        "padding_bottom": "1em",
        "backdrop_filter": "blur(10px)",
    },
    "#sidebar": {
        "width": "250px",
        "position": "fixed",
        "height": "100%",
        "left": "0px",
        "top": "0px",
        "align_items": "left",
        "z_index": "10",
        "backdrop_filter": "blur(10px)",
        "padding": "2em",
    },
    "#sidebar_vstack_header": {
        "font_family": FONT_FAMILY,
        "size": "7"
    },
    "#sidebar_header": {
        "width": "100%",
        "spacing": "7"
    },
    "#sidebar_vstack_links": {
        "padding_y": "1em"
    },
    ".sidebar_link": {
        "width": "100%",
        "border_radius": "8px",
    },
    ".sidebar_link_button": {
        "align": "center",
        "direction": "row",
        "font_family": FONT_FAMILY,

    },
    ".sidebar_link:hover": {
        "background": "rgba(255, 255, 255, 0.1)",
        "backdrop_filter": "blur(10px)",
    },
    ".content": {
        "background_color": rx.color("mauve", 2),
        "padding": "2em",
        "min_height": "calc(100vh - 50px - 2em)"
    },
    "#video-feed": {
        "padding_top": "2em",
        "padding_bot": "2em"
    },
    rx.section: {
        "margin_bottom": "2em"
    },
    rx.chakra.grid: {
        "width": "100%"
    }

}
