#!/usr/bin/env python3

"""
    simple script to check multiple http endpoints for
    their return codes and display a dashboard accordingly
"""

import traceback
import logging
import schedule
import time
import checkhttpconfig
from endpoint import EndpointYamlConfig
from endpoint import Endpoint

# configure logger
# http://docs.python-guide.org/en/latest/writing/logging/
logger = logging.getLogger()
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
# by default set logger to info. can be overwritten by checkhttpconfig.loglevel
logger.setLevel(logging.INFO)

def application():
    """
        main function
    """
    try:
        # initialize the configuration
        logger.info('Started checkhttp app')
        logger.info('Load app configuration')
        # we want the config to be available in all functions
        global config
        config = checkhttpconfig.CheckHttpConfig()
        # set the log level
        if config.loglevel == "info":
            logger.setLevel(logging.INFO)
        if config.loglevel == "debug":
            logger.setLevel(logging.DEBUG)

        # check if the app needs to run the checks
        if config.enable_checks.lower() in ['yes', 'true', 1]:
            try:
                # load configuration
                url_configuration = EndpointYamlConfig(config.yaml_config_file)
            except:
                raise FileNotFoundError

        # with the configuration in place we can create a list of endpoints to monitor
        endpoints = []
        for e in url_configuration.yaml:
            try:
                endpoints.append(Endpoint(**e))
            except:
                logger.warn("Not able to load entrypoint definition for '{}'.".format(e['id']))
                pass

        #start_response('200 OK', [('Content-Type','text/html')])
        #return "bluub"


    except Exception as err:
        logger.error(err)
        traceback.print_exc()



if __name__ == '__main__':
    logger.info('jaja')
    application()
