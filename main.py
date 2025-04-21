from utime import sleep


def loop():
    try:
        print("Hello World!")
    except Exception as e:
        print(e)
    finally:
        print("Reiniciando o sistema em 10 segundos...")
        sleep(10)


if __name__ == "__main__":
    try:
        while True:
            loop()
    except:
        pass
    finally:
        print("Sistema encerrado!")
