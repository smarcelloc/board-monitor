from network import WLAN, STA_IF
from logger import LOG_INFO
from utime import sleep
from ubinascii import hexlify


class WiFi:
    def __init__(self, ssid: str, password: str):
        self._ssid = ssid
        self._password = password
        self._wlan = WLAN(STA_IF)
        self._wlan.active(True)
        self._max_retries = 20
        self._retry_interval = 2

    def connect(self):
        if self.is_connected():
            return
        self._wlan.connect(self._ssid, self._password)
        retry = 0
        while not self.is_connected():
            if retry > self._max_retries:
                raise Exception("Não foi possível conectar ao WiFi!")
            LOG_INFO("Tentando conectar ao WiFi...")
            sleep(self._retry_interval)
            retry += 1

    def disconnect(self):
        if self.is_connected():
            self._wlan.disconnect()
        self._wlan.active(False)

    def is_connected(self) -> bool:
        return self._wlan.isconnected()

    def get_mac(self) -> str:
        mac = self._wlan.config("mac")
        return hexlify(mac).decode("utf-8")

    def get_ip(self) -> str:
        return self._wlan.ifconfig()[0]
