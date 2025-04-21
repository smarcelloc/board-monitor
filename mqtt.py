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
        if self.is_connected():
            self.__client.disconnect()

    def is_connected(self) -> bool:
        try:
            self.__client.ping()
            return True
        except Exception as e:
            return False

    def publish(self, topic: str, message: str):
        self.__client.publish(topic=topic, msg=message)
