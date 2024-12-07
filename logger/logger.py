from abc import ABC, abstractmethod
from typing import List
import json
import logging


class LogInfo:
    def __init__(self, server_domain_name: str, ip: str, attack_type: str, timeout: str, timestamp: str):
        self.server_domain_name = server_domain_name
        self.ip = ip
        self.attack_type = attack_type
        self.timeout = timeout
        self.timestamp = timestamp

    def data_to_dict(self):
        return \
            {
                "timestamp": self.timestamp,
                "domain": self.server_domain_name,
                "ip": self.ip,
                "attack type": self.attack_type,
                "timeout": self.timeout
            }


class _Ilogger(ABC):

    @abstractmethod
    def log(self, log_info: LogInfo):
        pass

    @abstractmethod
    def get_logged_data(self) -> List[LogInfo]:
        pass


class _InnerLogger(_Ilogger):
    def __init__(self):
        self.logger = logging.getLogger("InnerLogger")
        handler = logging.FileHandler("waf_system.log")
        handler.setFormatter(logging.Formatter('%(message)s'))
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.INFO)

    def log(self, log_info: LogInfo):
        self.logger.info(json.dumps(log_info.data_to_dict()))

    def get_logged_data(self):
        with open("waf_system.log", "r") as file:
            return file.read()


class _OuterLogger(_Ilogger):
    def __init__(self):
        pass

    def log(self, log_info: LogInfo):
        pass

    def get_logged_data(self) -> List[LogInfo]:
        pass


class Logger(_Ilogger):
    def __init__(self):
        self.innerLoger = _InnerLogger()
        self.outerLoger = _OuterLogger()

    def log(self, log_info: LogInfo):
        self.innerLoger.log(log_info)
        self.outerLoger.log(log_info)

    def get_logged_data(self) -> List[LogInfo]:
        return self.innerLoger.get_logged_data()


if __name__ == "__main__":
    iner = _InnerLogger()
    data = LogInfo("mysite.com", "123.233.32.432","XSS","32d","2024-12-05T16:30:00Z")
    iner.log(data)
    print(iner.get_logged_data())