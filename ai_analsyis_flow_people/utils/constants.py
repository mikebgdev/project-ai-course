from __future__ import annotations

import reflex as rx
import os
from dotenv import load_dotenv

load_dotenv()

RABBITMQ_HOST = os.getenv("RABBIT_HOST")
RABBITMQ_PORT_API = os.getenv("RABBIT_PORT_API")
RABBITMQ_API_URL = "http://" + RABBITMQ_HOST + ":" + RABBITMQ_PORT_API + "/api"
RABBITMQ_USERNAME = os.getenv("RABBIT_USER")
RABBITMQ_PASSWORD = os.getenv("RABBIT_PASSWORD")

MONGODB_HOST = os.getenv("MONGODB_HOST")
MONGODB_PORT_API = os.getenv("MONGODB_PORT_API")
MONGODB_API_URL = "http://" + MONGODB_HOST + ":" + MONGODB_PORT_API + "/api"

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

DOC_INDEX = "docs/Index.md"
DOC_ALL = 'README.md'

JSON_PERSONS = './notebooks/data/proyecto_ia_arch.persons.json'
JSON_TRACKS = './notebooks/data/proyecto_ia_arch.tracks.json'
