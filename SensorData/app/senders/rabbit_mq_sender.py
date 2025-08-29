import pika
import json

from ..dto.prediction_dto import PredictionDTO


class RabbitMQSender:


    def __init__(self, host='localhost'):

        self.host = host
        self.connection = None
        self.channel = None

    def _connect(self):
        try:
            self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=self.host))
            self.channel = self.connection.channel()
            print("Connessione a RabbitMQ stabilita con successo.")
        except Exception as e:
            print(f"Errore: Impossibile connettersi a RabbitMQ su host '{self.host}'. Dettagli: {e}")
            raise

    def publish_sensor_data(self, sensor_data: dict, queue_name='data-sensor-queue'):
        """
        Pubblica dati del sensore sulla coda specificata

        Args:
            sensor_data: Oggetto dict con i dati da inviare
            queue_name: Nome della coda (default: 'data-sensor-queue')
        """
        return self.publish_message(queue_name, sensor_data)


    def publish_message(self, queue_name, message_dict):

        try:
            self._connect()
            self.channel.queue_declare(queue=queue_name, durable=True)
            message_body = json.dumps(message_dict)

            self.channel.basic_publish(
                exchange='',
                routing_key=queue_name,
                body=message_body,
                properties=pika.BasicProperties(
                    delivery_mode=2,
                ))

            print(f" [x] Messaggio inviato a RabbitMQ sulla coda '{queue_name}': {message_body}")

        except Exception as e:
            print(f"Errore durante la pubblicazione del messaggio su RabbitMQ: {e}")
        finally:
            if self.connection and self.connection.is_open:
                self.connection.close()
                print("Connessione a RabbitMQ chiusa.")