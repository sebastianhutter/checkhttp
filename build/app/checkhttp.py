#!/usr/bin/env python3

"""
    simple script to check multiple http endpoints for
    their return codes and display a dashboard accordingly
"""

import traceback
import logging
import schedule
import time

import json

from threading import Timer

from bottle import Bottle, route, run, template, request

from checkhttpconfig import CheckHttpConfig
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


def initialize(config):
    """
        intialize configuration file
    """
    try:
        # initialize the configuration
        logger.info('Started checkhttp app')
        logger.info('Load app configuration')
        # we want the config to be available in all functions

        # set the log level
        if config.loglevel == "info":
            logger.setLevel(logging.INFO)
        if config.loglevel == "debug":
            logger.setLevel(logging.DEBUG)
    except:
        raise

def get_urls(config):
    """
        load yaml config file with urls
    """

    try:
        # load configuration
        url_configuration = EndpointYamlConfig(config.yaml_config_file)
        return url_configuration.yaml
    except:
        raise FileNotFoundError

def get_endpoints(urls, config):
    """
        get all endpoints from config
    """

    endpoints = []
    for e in urls:
        try:
            # now before we create the endpoint object lets see if we specified credentials
            # if not we will add the credentials from the environment by default
            if not 'credentials' in e or not 'username' in e['credentials'] or not 'password' in e['credentials']:
                e['credentials'] = {'username': config.http_user, 'password': config.http_pass}
            endpoints.append(Endpoint(**e))
        except:
            logger.warn("Not able to load entrypoint definition for '{}'.".format(e['id']))
            pass

    return endpoints

def check_endpoints(endpoints, wait_time):
    """
       run checks against all enabled endpoints
    """

    for e in endpoints:
        logger.info ("Checking endpoint '{}' with url '{}'".format(e.id,e.url))
        e.get_status_code()

    Timer(int(wait_time), check_endpoints, args=(endpoints,wait_time)).start()


# ------------------
# initialize bootle
# ------------------
app = Bottle()

@app.route('/')
@app.route('/dashboard')
def dashboard():
    # if someone requests json we deliver all endpoint info via json
    # else we render a template
    if request.headers.get('Accept') == 'application/json':
        return json.dumps(list(map(lambda x:x.return_json_dict(),endpoints)))
    else:
        return template('dashboard', endpoints=endpoints)

# ------------------
# main
# ------------------

if __name__ == '__main__':
    try:
        # load configruation
        app_config = CheckHttpConfig()
        # load configuration file
        initialize(app_config)
        # get all urls
        app_urls = get_urls(app_config)
        # get all endpoints
        endpoints = get_endpoints(app_urls, app_config)
        # check all endpoints
        check_endpoints(endpoints, app_config.wait_time)
        # start bottle app
        run(app, host='0.0.0.0', port=int(app_config.http_port))
    except Exception as err:
        logger.error(err)
        traceback.print_exc()
