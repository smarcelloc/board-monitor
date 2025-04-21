from utime import sleep
from logger import LOG_INFO, LOG_ERROR
from app import App

app = App()


def app_start():
    while True:
        try:
            app.start()
            return
        except Exception as e:
            LOG_ERROR(e)
            LOG_INFO("Reiniciando o sistema em 10 segundos...")
            sleep(10)


def app_shutdown():
    app.shutdown()


if __name__ == "__main__":
    try:
        app_start()
    except:
        pass
    finally:
        app_shutdown()
