# config.py

import os
from configparser import ConfigParser


class MailServiceConfig:
    def __init__(self, config_file: str = 'config.ini'):
        self.config = ConfigParser()
        self.config.read(config_file)

    @property
    def base_url(self):
        return os.getenv(
            'MAIL_SERVICE_BASE_URL',
            self.config.get('DEFAULT', 'BASE_URL', fallback='https://www.1secmail.com/api/v1/')
        )

    @property
    def timeout(self):
        return int(os.getenv(
            'MAIL_SERVICE_TIMEOUT',
            self.config.get('DEFAULT', 'TIMEOUT', fallback='10')
        ))