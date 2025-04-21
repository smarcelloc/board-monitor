from logger import Logger, LOG_INFO, LOG_ERROR, LOG_LEVEL
from config import *
from network import WLAN, STA_IF
from utime import sleep
from ujson import loads as json_load


class App:

    def __init__(self):
        self._wlan = WLAN(STA_IF)
        self._wlan.active(True)

    def initialize_logger(self):
        Logger.level = LOG_LEVEL[CONFIG_LOG_LEVEL]
        Logger.console = CONFIG_LOG_CONSOLE
        Logger.path = CONFIG_LOG_PATH
        Logger.max_size_kb = CONFIG_LOG_MAX_SIZE_KB
        LOG_INFO("Sistema iniciado!")

    def connect_wifi(self):
        if self._wlan.isconnected():
            LOG_INFO("Conectado ao WiFi!")
            return
        self._wlan.connect(CONFIG_WIFI_SSID, CONFIG_WIFI_PASSWORD)
        retry = 0
        while not self._wlan.isconnected():
            if retry > 20:
                raise Exception("Não foi possível conectar ao WiFi!")
            LOG_INFO("Tentando conectar ao WiFi...")
            sleep(2)
            retry += 1
        LOG_INFO("Conectado ao WiFi!")
