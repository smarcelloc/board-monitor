from umqttsimple import MQTTClient
from utime import time


class MQTT:

    def __init__(self, client: str, host: str, port: int, username: str, password: str):
        self.__client = MQTTClient(
            client_id=client,
            server=host,
            port=port,
            user=username,
            password=password,
        )

    def connect(self):
        self.__client.connect()

    def disconnect(self):
        try:
            self.__client.disconnect()
        except Exception as e:
            pass

    def publish(self, topic: str, message: str):
        self.__client.publish(topic=topic, msg=message)
