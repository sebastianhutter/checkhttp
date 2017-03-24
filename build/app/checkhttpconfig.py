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

        # the yaml configfile to use
        self.endpointfile = os.getenv('CHECKHTTP_YAML','config.yml')

        # is the app running the http checks
        self.enable_checks = os.getenv('CHECKHTTP_ENABLE_CHECKS', 'true')

        # the url or local file path to the yaml config file with
        # url definitons
        self.yaml_config_file = os.getenv('CHECKHTTP_YAML_FILE', '')
