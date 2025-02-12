from typing import List
import json
import logging
import os

INNER_LOG_PATH = "logs\\inner"
OUTER_LOG_PATH = "logs\\outer"
INNER_LOG_FILE_NAME = "waf_system.log"


class LogInfo:
    def _protect_logger(self):
        #replace the salshed to prevent file traversal
        self.server_domain_name = self.server_domain_name.replace("/","")
        self.server_domain_name = self.server_domain_name.replace("\\","")
    def __init__(self, server_domain_name: str, ip: str, attack_type: str, timeout: str, timestamp: str):
        self.server_domain_name = server_domain_name
        self.ip = ip
        self.attack_type = attack_type
        self.timeout = timeout
        self.timestamp = timestamp
        self._protect_logger()

    def data_to_dict(self):
        return \
            {
                "timestamp": self.timestamp,
                "domain": self.server_domain_name,
                "ip": self.ip,
                "attack type": self.attack_type,
                "timeout": self.timeout
            }


class _InnerLogger:

    def __init__(self):
        os.makedirs(INNER_LOG_PATH, exist_ok=True)

        self.log_file_path = f"{INNER_LOG_PATH}\\{INNER_LOG_FILE_NAME}"
        self.logger = logging.getLogger("InnerLogger")
        handler = logging.FileHandler(self.log_file_path)
        handler.setFormatter(logging.Formatter('%(message)s'))
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.INFO)

    def log(self, log_info: LogInfo):
        self.logger.info(json.dumps(log_info.data_to_dict()))

    def get_logged_data(self):
        with open(self.log_file_path, "r") as file:
            return file.read()


class _OuterLogger:
    def _protect_logger(self):
        #replace the salshed to prevent file traversal
        self.server_domain_name = self.log_dir.replace("/","")
        self.server_domain_name = self.log_dir.replace("\\","")
    def __init__(self):
        self.log_dir = OUTER_LOG_PATH
        self._protect_logger()
        os.makedirs(self.log_dir, exist_ok=True)
        self.loggers = {}
    def _get_website_name_without_speacial_characters(self,website_name:str)->str:
        """func is for preventing attackers to do file traversal into our log system and get classified data"""
        new_website_name = ""
        for letter in website_name:
            if letter.isalpha() or letter.isdigit():
                new_website_name+=letter
        return new_website_name
    def _get_logger(self, website_name):
        if website_name not in self.loggers:
            logger = logging.getLogger(f"OuterLogger_{website_name}")
            handler = logging.FileHandler(f"{self.log_dir}/{website_name}.log")
            handler.setFormatter(logging.Formatter('%(message)s'))  # JSON format
            logger.addHandler(handler)
            logger.setLevel(logging.INFO)
            self.loggers[website_name] = logger
        return self.loggers[website_name]

    def log(self, website_name, message):
        logger = self._get_logger(website_name)
        logger.info(json.dumps(message.data_to_dict()))

    def get_logged_data(self, website_name):
        log_file = f"{self.log_dir}/{website_name}.log"
        if os.path.exists(log_file):
            with open(log_file, "r") as file:
                return file.read()
        return None


class Logger:
    def __init__(self):
        self.innerLoger = _InnerLogger()
        self.outerLoger = _OuterLogger()

    def log(self, log_info: LogInfo):
        self.innerLoger.log(log_info)
        self.outerLoger.log(log_info.data_to_dict()["domain"], log_info)

    def get_logged_data(self, website: str = "") -> str:
        """
        the function fetches a log file
        :param website: the name of the website the log is documenting -> str
        if no name is entered it fetches the inner log file -> None/""
        :return: the data from the log file -> str
        """
        if website == "":
            return self.innerLoger.get_logged_data()
        return self.outerLoger.get_logged_data(website)


if __name__ == "__main__":
    logger = Logger()
    data = LogInfo("../inner/waf_system", "123.233.32.432", "XSS", "32d", "2024-12-05T16:30:00Z")
    logger.log(data)
    print(logger.get_logged_data())
