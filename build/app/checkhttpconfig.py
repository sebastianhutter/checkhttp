#!/usr/bin/env python3
"""
    parse configuration for script.
    the whole config is done via env variables and vault
"""

import os

class CheckHttpConfig(object):

    def __init__(self):
        """
            initialize and check configuration
        """

        # set the loglevel
        self.loglevel = os.getenv('CHECKHTTP_LOGLEVEL','DEBUG')

        # the url or local file path to the yaml config file with
        # url definitons
        self.yaml_config_file = os.getenv('CHECKHTTP_YAML_FILE', '')

        # set global username and password for http endpoints
        self.http_user = os.getenv('CHECKHTTP_HTTP_USER', '')
        self.http_pass = os.getenv('CHECKHTTP_HTTP_PASS', '')

        # listening ip
        self.ip = os.getenv('CHECKHTTP_IP', '0.0.0.0')
        # http port for the server
        self.http_port = os.getenv('CHECKHTTP_HTTP_PORT', '8080')

        # waiting time between requests
        self.wait_time = os.getenv('CHECKHTTP_WAIT_TIME', '60')

        # timezone for the displayed times
        self.timezone = os.getenv('CHECKHTTP_TIMEZONE', 'Europe/Zurich')