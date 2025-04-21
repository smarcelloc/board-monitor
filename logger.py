from utime import localtime

LOG_LEVEL = {"DEBUG": 10, "INFO": 20, "WARNING": 30, "ERROR": 40, "FATAL": 50}


class Logger:
    level: int = LOG_LEVEL["ERROR"]
    console: bool = False
    path: str = "log.txt"
    max_size_kb: int = 10

    @staticmethod
    def log(level: str, message: str):
        if not LOG_LEVEL[level] >= Logger.level:
            return

        log_formatted = f"[{Logger._get_timestamp()}] [{level}]: {message}"

        if Logger.console:
            print(log_formatted)

    @staticmethod
    def _get_timestamp():
        now = localtime()
        return "{:04d}-{:02d}-{:02d} {:02d}:{:02d}:{:02d}".format(*now[:6])


def LOG_DEBUG(message: str):
    Logger.log("DEBUG", message)


def LOG_INFO(message: str):
    Logger.log("INFO", message)


def LOG_WARNING(message: str):
    Logger.log("WARNING", message)


def LOG_ERROR(message: str):
    Logger.log("ERROR", message)


def LOG_FATAL(message: str):
    Logger.log("FATAL", message)
