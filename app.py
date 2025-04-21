from logger import Logger, LOG_INFO, LOG_ERROR, LOG_LEVEL
from config import *


class App:

    def __init__(self):
        pass

    def initialize_logger(self):
        Logger.level = LOG_LEVEL[CONFIG_LOG_LEVEL]
        Logger.console = CONFIG_LOG_CONSOLE
        Logger.path = CONFIG_LOG_PATH
        Logger.max_size_kb = CONFIG_LOG_MAX_SIZE_KB
        LOG_INFO("Sistema iniciado!")
