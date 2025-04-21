from utime import localtime
from os import stat
from _thread import get_ident

LOG_LEVEL = {"DEBUG": 10, "INFO": 20, "WARNING": 30, "ERROR": 40, "FATAL": 50}


class Logger:
    level: int = LOG_LEVEL["ERROR"]
    console: bool = False
    path: str = "log.txt"
    max_size_kb: int = 10
    thread_names = {}

    @staticmethod
    def log(level: str, message: str):
        try:
            if not LOG_LEVEL[level] >= Logger.level:
                return
            log_formatted = f"[{Logger._get_timestamp()}] [{level}] [Thread {Logger._get_thread_name()}]: {message}"
            if Logger.console:
                print(log_formatted)
            if Logger.path:
                Logger._write_log_to_file(log_formatted)
        except Exception as e:
            pass

    @staticmethod
    def _get_timestamp() -> str:
        now = localtime()
        return "{:04d}-{:02d}-{:02d} {:02d}:{:02d}:{:02d}".format(*now[:6])

    @staticmethod
    def _get_thread_name() -> str:
        thread_id = get_ident()
        return Logger.thread_names.get(thread_id, "Desconhecido")

    @staticmethod
    def set_thread_name(name: str):
        thread_id = get_ident()
        Logger.thread_names[thread_id] = name

    @staticmethod
    def _write_log_to_file(log_message: str):
        mode = "w" if Logger._is_file_exceeded_size() else "a"
        with open(Logger.path, mode) as log_file:
            log_file.write(log_message + "\n")
            log_file.flush()

    @staticmethod
    def _is_file_exceeded_size() -> bool:
        try:
            file_size_byte = stat(Logger.path)[6]
            return file_size_byte > (Logger.max_size_kb * 1024)
        except Exception as e:
            return True


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
