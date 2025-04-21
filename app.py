from logger import Logger, LOG_INFO, LOG_ERROR, LOG_DEBUG, LOG_LEVEL
from config import *
from wifi import WiFi
from utime import sleep
from ujson import loads as json_load
from ntptime import settime
from mqtt import MQTT


class App:

    def __init__(self):
        self._wifi = None
        self._mqtt = None

    def shutdown(self):
        self.disconnect_wifi()
        self.disconnect_mqtt()
        LOG_INFO("Sistema encerrado!")

    def disconnect_wifi(self):
        if not self._wifi:
            return
        try:
            self._wifi.disconnect()
            LOG_INFO("Desconectado do WiFi!")
        except Exception as e:
            LOG_ERROR(f"Erro ao desconectar do WiFi: {e}")

    def disconnect_mqtt(self):
        if not self._mqtt:
            return
        try:
            self._mqtt.disconnect()
            LOG_INFO("Desconectado do MQTT!")
        except Exception as e:
            LOG_ERROR(f"Erro ao desconectar do MQTT: {e}")

    def initialize_logger(self):
        Logger.level = LOG_LEVEL[CONFIG_LOG_LEVEL]
        Logger.console = CONFIG_LOG_CONSOLE
        Logger.path = CONFIG_LOG_PATH
        Logger.max_size_kb = CONFIG_LOG_MAX_SIZE_KB
        LOG_INFO("Sistema iniciado!")

    def connect_wifi(self):
        self._wifi = WiFi(
            ssid=CONFIG_WIFI_SSID,
            password=CONFIG_WIFI_PASSWORD,
        )
        self._wifi.connect()
        LOG_INFO("Conectado ao WiFi!")
        LOG_DEBUG(f"IP Address: {self._wifi.get_ip()}")
        LOG_DEBUG(f"MAC Address: {self._wifi.get_mac()}")

    def sync_time(self):
        settime()
        LOG_INFO("Hora sincronizada com o servidor NTP!")

    def connect_mqtt(self):
        try:
            self._mqtt = MQTT(
                client=self._wifi.get_mac(),
                host=CONFIG_MQTT_HOST,
                port=CONFIG_MQTT_PORT,
                username=CONFIG_MQTT_USERNAME,
                password=CONFIG_MQTT_PASSWORD,
            )
            self._mqtt.connect()
            LOG_INFO("Conectado ao MQTT!")
        except Exception as e:
            raise Exception(f"Erro ao conectar ao MQTT: {e}")
