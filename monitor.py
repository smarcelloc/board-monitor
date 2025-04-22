from event_loop import EventLoop
from logger import LOG_INFO, LOG_ERROR, LOG_DEBUG
from utime import localtime, mktime
from faker import Faker
from re import sub as re_sub


class PayloadData:
    def __init__(self):
        self.checksum: int = 0
        self.length: int = 0
        self.timestamp: int = 0
        self.board_mac: str = ""
        self.temperature: float = 0.0  # Temperatura em graus Celsius (°C)
        self.humidity: float = 0.0  # Umidade em porcentagem (%)
        self.pressure: float = 0.0  # Pressão em hectopascais (hPa)


class Monitor:

    def __init__(self, mqtt, board_mac: str):
        self._mqtt = mqtt
        self._board_mac = board_mac
        self._data = PayloadData()
        self._payload = ""

    async def run(self):
        while True:
            try:
                self._data = PayloadData()
                self._set_timestamp()
                self._set_board_mac()
                self._set_board_temperature()
                self._set_board_humidity()
                self._set_board_pressure()
                self._set_payload()
                self._publish_payload()
            except Exception as e:
                LOG_ERROR(f"Falha em publicar o payload: {e}")
            finally:
                await EventLoop.sleep_ms(10000)

    def _set_timestamp(self):
        self._data.timestamp = mktime(localtime())

    def _set_board_mac(self):
        self._data.board_mac = self._board_mac

    def _set_board_temperature(self):
        self._data.temperature = Faker.temperature()

    def _set_board_humidity(self):
        self._data.humidity = Faker.humidity()

    def _set_board_pressure(self):
        self._data.pressure = Faker.pressure()

    def _set_payload(self):
        self._payload = ""
        self._payload += "{:>08x}".format(self._data.timestamp)
        self._payload += "{:>012s}".format(self._data.board_mac)
        self._payload += self._get_float_encode(value=self._data.temperature, places=1)
        self._payload += self._get_float_encode(value=self._data.humidity, places=1)
        self._payload += self._get_float_encode(value=self._data.pressure, places=1)

        self._data.length = self._get_payload_length()
        self._payload = "{:>02x}".format(self._data.length) + self._payload

        self._data.checksum = self._get_payload_checksum()
        self._payload = "{:>02x}".format(self._data.checksum) + self._payload

    def _get_float_encode(self, value: float, places: int, fmt: str = "{:>04x}") -> str:
        negative = value < 0
        value = round(value, places)
        value = re_sub(r"[^\d]", "", str(value))
        return ("0" if negative else "1") + fmt.format(int(value))

    def _get_payload_length(self) -> int:
        return int(len(self._payload) / 2)

    def _get_payload_checksum(self) -> int:
        checksum = 78
        for character in self._payload:
            checksum ^= ord(character)
        return checksum

    def _publish_payload(self):
        LOG_DEBUG(f"Publicando o payload: {self._payload}")
        LOG_DEBUG(f"Dados do payload: {self._data.__dict__}")
        self._mqtt.publish(topic="monitor", message=self._payload)
        LOG_INFO("Publicado o payload com sucesso!")
