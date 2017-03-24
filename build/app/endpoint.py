#!/usr/bin/env python3

"""
    load http endpoints via yaml
    monitor http endpoints
    store results
"""

# initialize logger
import logging
logger = logging.getLogger(__name__)

from urllib.parse import urlparse
from requests.auth import HTTPBasicAuth
import requests
import json
import yaml
from datetime import datetime


class EndpointYamlConfig (object):
    """
        class to parse the yaml config containing all
        urls to check

    """

    def __init__(self, file):
        """
            get and parse the yaml configuration file
        """

        # load the configuraiton into memory
        try:
            parsed_source = urlparse(file)
            if parsed_source.scheme in ['http', 'https']:
                response = requests.get(file)
                self.source = response.content
            else:
                with open(file, 'r') as source:
                    self.source = source.read()
        except:
            raise

        # try to parse the config
        try:
            self.yaml = yaml.load(self.source)['checkhttp']
        except:
            raise


class Endpoint (object):
    """
        represents http endpoint
    """
    def __init__(self, id, url, request_type="GET", http_codes = [200], credentials = {}, basic_auth = False, enabled = True):
        """
            initialize an url object
        """

        self.enabled = enabled
        self.id = id
        self.url = url
        self.request_type = request_type.upper()
        self.http_codes = http_codes
        self.credentials = credentials
        self.basic_auth = basic_auth
        self.enabled = enabled
        self.last_status_code = None
        self.status_code = None
        self.status_code_time = None

        # validate paramemters
        if not self.id:
            raise ValueError("Invalid id specified")

        if not self.url or not urlparse(self.url).scheme in ['http', 'https']:
            raise ValueError("Invalid url specified")

        if not self.request_type or self.request_type != 'GET' and self.request_type != 'POST':
            raise ValueError('Invalid request type specified')

        if not self.http_codes:
            logger.warn('No expected http codes defined. Set to 200')
            self.http_codes = [200]

        if 'username' in self.credentials:
            if not self.credentials['username']:
                logger.warn('No username defined. Disable basic auth for url')
                self.basic_auth = False
        else:
            logger.warn('No username defined. Disable basic auth for url')
            self.basic_auth = False

        if 'password' in self.credentials:
            if not self.credentials['password']:
                logger.warn('No password defined. Disable basic auth for url')
                self.basic_auth = False
        else:
            logger.warn('No password defined. Disable basic auth for url')
            self.basic_auth = False

        # if proper username and password are defined create a basic auth object
        if self.basic_auth:
            self.httpauth = HTTPBasicAuth(self.credentials['username'], self.credentials['password'])
        else:
            self.httpauth = None


    def get_status_code(self):
        """
            request url and store status code
        """
        if self.enabled:
            try:
                if self.request_type == 'GET':
                    r = requests.get(self.url, auth=self.basic_auth)
                if self.request_type == 'POST':
                    r = requests.post(self.url, auth=self.basic_auth)

                # save the return value
                self.last_status_code = self.status_code
                self.status_code = r.status_code
                self.status_code_time = datetime.now().time()
            except Exception as exception:
                logger.warn("Unable to connect to url. Disable URL".format(exception.errno))
                pass
        else:
            logger.debug("Url is set to disabled. not executing request")

    def return_status_code(self):
        """
            return the statuscode for the url endpoint
        """
        if self.status_code:
            return self.status_code

    def return_state(self):
        """
            returns the status of the url endpoint (true = all good, false = everything bad)
            it returns true if the received status code of the requests equals one of the specified
            codes in https codes
        """
        if self.status_code in self.http_codes:
            return True
        else:
            return False


    def return_json(self):
        """
            return the endpoint object as json
        """
        data = {
            "enabled"           : self.enabled,
            "id"                : self.id,
            "url"               : self.url,
            "request_type"      : self.request_type,
            "http_codes"        : self.http_codes,
            "status_code"       : self.status_code,
            "last_status_code"  : self.last_status_code,
            "state"             : self.return_state()
        }
        return json.dumps(data)