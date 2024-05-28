import reflex as rx


def get_content(markdown):
    with open(markdown, 'r', encoding='utf-8') as file:
        content = file.read()

    return content


def markdown_component(markdown):
    return rx.markdown(get_content(markdown))
