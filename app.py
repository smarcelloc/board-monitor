from logger import Logger, LOG_INFO, LOG_ERROR, LOG_DEBUG, LOG_LEVEL
from config import *
from wifi import WiFi
from utime import sleep
from ujson import loads as json_load
from ntptime import settime
from mqtt import MQTT
from event_loop import EventLoop
from monitor import Monitor


class App:

    def __init__(self):
        self._wifi = None
        self._mqtt = None
        self._event_loop = None

    def start(self):
        self.initialize_logger()
        self.connect_wifi()
        self.sync_time()
        self.connect_mqtt()
        self.event_loop_run()

    def shutdown(self):
        LOG_INFO("Solicitado o encerramento do sistema")
        self.event_loop_stop()
        self.disconnect_mqtt()
        self.disconnect_wifi()
        LOG_INFO("Sistema encerrado!")

    def event_loop_stop(self):
        if not self._event_loop:
            return
        try:
            self._event_loop.stop()
            self._event_loop = None
            LOG_INFO("Finalizado os processos do sistema")
        except Exception as e:
            LOG_ERROR(f"Erro ao finalizar os processos do sistema: {e}")

    def disconnect_mqtt(self):
        if not self._mqtt:
            return
        try:
            self._mqtt.disconnect()
            self._mqtt = None
            LOG_INFO("Desconectado do MQTT!")
        except Exception as e:
            LOG_ERROR(f"Erro ao desconectar do MQTT: {e}")

    def disconnect_wifi(self):
        if not self._wifi:
            return
        try:
            self._wifi.disconnect()
            self._wifi = None
            LOG_INFO("Desconectado do WiFi!")
        except Exception as e:
            LOG_ERROR(f"Erro ao desconectar do WiFi: {e}")

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
        try:
            settime()
            LOG_INFO("Horário sincronizado com o servidor NTP!")
        except Exception as e:
            raise Exception(f"Falhou em sincronizar o horário com servidor NTP: {e}")

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

    def event_loop_run(self):
        try:
            self._event_loop = EventLoop()
            self._add_task_monitor()
            self._event_loop.run()
        except Exception as e:
            raise Exception(f"Erro ao inicializar o Event Loop: {e}")

    def _add_task_monitor(self):
        monitor = Monitor(self._mqtt)
        self._event_loop.add_task("monitor", monitor.run())
        self._event_loop.add_task("monitor1", monitor.run())
