from event_loop import EventLoop
from logger import LOG_INFO, LOG_ERROR


class Monitor:

    def __init__(self, mqtt):
        self._mqtt = mqtt

    async def run(self):
        while True:
            try:
                self._mqtt.publish(topic="monitor", message="ok")
                LOG_INFO("Publicado os dados de monitoramento da placa")
            except Exception as e:
                LOG_ERROR(f"Falhou publicar os dados de monitoramento da placa: {e}")
            finally:
                await EventLoop.sleep_ms(30000)
