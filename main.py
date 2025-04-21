from utime import sleep
from logger import LOG_INFO, LOG_ERROR
from app import App

app = App()


def loop():
    try:
        app.initialize_logger()
        app.connect_wifi()
        app.sync_time()
        app.connect_mqtt()
    except Exception as e:
        LOG_ERROR(e)
    finally:
        LOG_INFO("Reiniciando o sistema em 10 segundos...")
        sleep(10)


if __name__ == "__main__":
    try:
        while True:
            loop()
    except:
        pass
    finally:
        app.shutdown()
