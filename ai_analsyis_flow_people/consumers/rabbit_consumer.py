import reflex as rx
import asyncio
import httpx
from ai_analsyis_flow_people.utils.constants import RABBITMQ_USERNAME, RABBITMQ_PASSWORD, RABBITMQ_API_URL


class DashboardRabbitMqState(rx.State):
    queues: int = 0
    consumers: int = 0
    connections: int = 0
    channels: int = 0
    incoming_messages: int = 0
    outgoing_messages: int = 0
    ready_messages: int = 0
    unacknowledged_messages: int = 0
    network_traffic_sent: int = 0
    network_traffic_received: int = 0
    exchanges: int = 0
    virtual_hosts: int = 0

    @rx.background
    async def update_metrics(self):
        auth = (RABBITMQ_USERNAME, RABBITMQ_PASSWORD)
        async with httpx.AsyncClient() as client:
            while True:
                try:
                    # Información de colas
                    queues_response = await client.get(
                        f"{RABBITMQ_API_URL}/queues?disable_stats=true&enable_queue_totals=true", auth=auth)
                    queues = queues_response.json()
                    async with self:
                        self.queues = len(queues)
                        self.ready_messages = sum(q['messages_ready'] for q in queues)
                        self.unacknowledged_messages = sum(q['messages_unacknowledged'] for q in queues)

                    # Información de consumidores
                    consumers_response = await client.get(f"{RABBITMQ_API_URL}/consumers", auth=auth)
                    consumers = consumers_response.json()
                    async with self:
                        self.consumers = len(consumers)

                    # Información de conexiones
                    connections_response = await client.get(f"{RABBITMQ_API_URL}/connections", auth=auth)
                    connections = connections_response.json()
                    async with self:
                        self.connections = len(connections)

                    # Información de canales
                    channels_response = await client.get(f"{RABBITMQ_API_URL}/channels", auth=auth)
                    channels = channels_response.json()
                    async with self:
                        self.channels = len(channels)

                    # Métricas de rendimiento
                    overview_response = await client.get(f"{RABBITMQ_API_URL}/overview", auth=auth)
                    overview = overview_response.json()
                    async with self:
                        self.incoming_messages = overview['message_stats'].get('publish', 0)
                        self.outgoing_messages = overview['message_stats'].get('deliver_get', 0)
                        self.network_traffic_sent = overview['message_stats'].get('confirm', 0)
                        self.network_traffic_received = overview['message_stats'].get('return_unroutable', 0)

                    # Información de exchanges
                    exchanges_response = await client.get(f"{RABBITMQ_API_URL}/exchanges", auth=auth)
                    exchanges = exchanges_response.json()
                    async with self:
                        self.exchanges = len(exchanges)

                    # Información de virtual hosts
                    vhosts_response = await client.get(f"{RABBITMQ_API_URL}/vhosts", auth=auth)
                    vhosts = vhosts_response.json()
                    async with self:
                        self.virtual_hosts = len(vhosts)

                except Exception as e:
                    print(f"Error fetching metrics: {e}")

                await asyncio.sleep(5)  # Actualiza cada 5 segundos
