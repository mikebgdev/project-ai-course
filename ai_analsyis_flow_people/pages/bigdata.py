import reflex as rx
import json
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from ai_analsyis_flow_people.components.navigation import navbar
from ai_analsyis_flow_people.components.template import template
from ai_analsyis_flow_people.components.graphs import stat_card


def read_data_from_json(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data


def process_data_track(data_list):
    df = pd.DataFrame(data_list)

    mean_df = pd.DataFrame(df['mean'].tolist(), columns=[f'mean_{i}' for i in range(8)])
    cov_df = pd.DataFrame([item for sublist in df['covariance'] for item in sublist],
                          columns=[f'cov_{i}' for i in range(8)])

    df = pd.concat([df, mean_df, cov_df], axis=1)

    df.drop(['mean', 'covariance'], axis=1, inplace=True)

    return df


persons_file = './notebooks/data/proyecto_ia_arch.persons.json'
tracks_file = './notebooks/data/proyecto_ia_arch.tracks.json'

data_person_list = read_data_from_json(persons_file)
processed_person_df = pd.DataFrame(data_person_list)

data_track_list = read_data_from_json(tracks_file)
processed_track_df = process_data_track(data_track_list)


def format_timestamp(timestamp):
    return pd.to_datetime(timestamp, unit='s')


def plot_person_durations_histogram(track_df):
    track_df['start_time'] = format_timestamp(track_df['start_time'])
    track_df['end_time'] = format_timestamp(track_df['end_time'])
    track_df['duration'] = track_df['end_time'] - track_df['start_time']
    fig = px.histogram(track_df, x='duration', nbins=20)
    fig.update_layout(title='Histograma de Duraciones de Tracks', xaxis_title='Duración del Track',
                      yaxis_title='Frecuencia')
    return fig


def plot_person_durations_over_time(track_df):
    track_df['start_time'] = format_timestamp(track_df['start_time'])
    track_df['end_time'] = format_timestamp(track_df['end_time'])
    track_df['duration'] = track_df['end_time'] - track_df['start_time']
    track_df = track_df.sort_values(by='start_time')
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=track_df['start_time'], y=track_df['duration'], mode='lines+markers'))
    fig.update_layout(title='Duración de Tracks a lo largo del tiempo', xaxis_title='Tiempo de inicio',
                      yaxis_title='Duración del Track')
    return fig


def plot_person_start_vs_end(track_df):
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(x=track_df['start_time'], y=track_df['end_time'], mode='markers', marker=dict(color='orange')))
    fig.update_layout(title='Tiempo de inicio vs Tiempo de fin de los Tracks', xaxis_title='Tiempo de inicio',
                      yaxis_title='Tiempo de fin')
    return fig


def plot_track_confidence_vs_time(track_df):
    track_df['time'] = format_timestamp(track_df['time'])
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=track_df['time'], y=track_df['conf'], mode='lines+markers'))
    fig.update_layout(title='Confianza del Track a lo largo del tiempo', xaxis_title='Tiempo', yaxis_title='Confianza')
    return fig


def plot_track_position(track_df):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=track_df['cord_x'], y=track_df['cord_y'], mode='markers'))
    fig.update_layout(title='Posición de los Tracks', xaxis_title='Coordenada X', yaxis_title='Coordenada Y')
    return fig


def generate_pie_chart(track_df):
    fig = px.pie(track_df, names='state', title='Distribución de Tracks por Estado')
    return fig


def prepare_data_stat_card():
    total_persons = int(processed_person_df['track_id'].count())
    total_tracks = int(processed_track_df['track_id'].count())
    average_confidence = round(processed_track_df['conf'].mean(), 2)
    active_tracks = int(processed_track_df[processed_track_df['state'] == 1]['track_id'].count())
    average_track_duration = round((processed_track_df['time'].max() - processed_track_df['time'].min()) / total_tracks,
                                   2)
    average_hits_per_track = round(processed_track_df['hits'].mean(), 2)

    return [
        ["Total Persons", total_persons],
        ["Total Tracks", total_tracks],
        ["Active Tracks", active_tracks],
        ["Average Confidence", average_confidence],
        ["Average Track Duration", average_track_duration],
        ["Average Hits per Track", average_hits_per_track]
    ]


def content_grid():
    return rx.chakra.grid(
        *[
            rx.chakra.grid_item(stat_card(*c), col_span=1, row_span=1)
            for c in prepare_data_stat_card()
        ],
        rx.chakra.grid_item(
            rx.heading("Duración del seguimiento de personas"),
            rx.plotly(data=plot_person_durations_histogram(processed_person_df)),
            col_span=3,
            row_span=2,
        ),
        rx.chakra.grid_item(
            rx.heading("Duración de Tracks a lo largo del tiempo"),
            rx.plotly(data=plot_person_durations_over_time(processed_person_df)),
            col_span=3,
            row_span=2,
        ),
        rx.chakra.grid_item(
            rx.heading("Tiempo de inicio vs Tiempo de fin de los Tracks"),
            rx.plotly(data=plot_person_start_vs_end(processed_person_df)),
            col_span=3,
            row_span=2,
        ),
        rx.chakra.grid_item(
            rx.heading("Confianza del Track a lo largo del tiempo"),
            rx.plotly(data=plot_track_confidence_vs_time(processed_track_df)),
            col_span=3,
            row_span=2,
        ),
        rx.chakra.grid_item(
            rx.heading("Posición de los Tracks"),
            rx.plotly(data=plot_track_position(processed_track_df)),
            col_span=3,
            row_span=2,
        ),
        rx.chakra.grid_item(
            rx.heading("Distribución de Tracks por Estado"),
            rx.plotly(data=generate_pie_chart(processed_track_df)),
            col_span=3,
            row_span=2,
        ),
        template_columns="repeat(6, 1fr)",
        width="100%",
        gap=6,
        row_gap=8,
    )


@template
def bigdata() -> rx.Component:
    return rx.box(
        navbar(heading="Dashboard Big Data"),
        rx.box(
            content_grid(),
            background_color=rx.color("mauve", 2),
            padding="2em",
            min_height="calc(100vh - calc(50px + 2em))",
        ),
        padding_top="calc(50px + 2em)",
        padding_left="250px",
    )
