"""rabbitmq_messenger.py
=======================
Modulo di messaggistica basato su RabbitMQ per Mercurius∞.

Fornisce funzioni semplici per pubblicare e consumare messaggi utilizzando il
protocollo AMQP tramite la libreria ``pika``. In assenza del server RabbitMQ le
funzioni restituiscono errori gestiti senza sollevare eccezioni critiche.
"""

from typing import Callable, Optional

import pika
from utils.logger import setup_logger

logger = setup_logger("RabbitMQMessenger")


def publish_message(queue: str, message: str, url: str = "amqp://guest:guest@localhost:5672/") -> bool:
    """Invia un messaggio alla coda specificata.

    Ritorna ``True`` se l'operazione è andata a buon fine, altrimenti ``False``.
    """
    try:
        params = pika.URLParameters(url)
        connection = pika.BlockingConnection(params)
        channel = connection.channel()
        channel.queue_declare(queue=queue, durable=True)
        channel.basic_publish(exchange="", routing_key=queue, body=message)
        connection.close()
        logger.info(f"[RabbitMQ] Sent to {queue}: {message}")
        return True
    except Exception as exc:
        logger.error(f"[RabbitMQ] publish failed: {exc}")
        return False


def consume_messages(queue: str, handler: Callable[[str], None], url: str = "amqp://guest:guest@localhost:5672/", limit: Optional[int] = None) -> None:
    """Consuma messaggi dalla coda chiamando ``handler`` per ogni messaggio.

    ``limit`` permette di definire quante messaggi leggere prima di chiudere la
    connessione (``None`` per ciclo infinito).
    """
    try:
        params = pika.URLParameters(url)
        connection = pika.BlockingConnection(params)
        channel = connection.channel()
        channel.queue_declare(queue=queue, durable=True)

        count = 0
        for method_frame, _properties, body in channel.consume(queue):
            handler(body.decode())
            channel.basic_ack(method_frame.delivery_tag)
            count += 1
            if limit and count >= limit:
                break
        channel.cancel()
        connection.close()
    except Exception as exc:
        logger.error(f"[RabbitMQ] consume failed: {exc}")
