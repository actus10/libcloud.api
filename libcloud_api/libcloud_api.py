# -*- coding: utf-8 -*-
from config import config
from flask import Flask
from flask_restful import Api
import logging

from resources.driver_resource import DriverResource
from utils import name_url


class libcloud_api(object):
    def __init__(self):
        self.config = config()
        self.clouds = []
        self.app = Flask(__name__)
        self.api = Api(self.app)
        self.resources = {}

    def build_controllers(self):
        providers = self.config.providers()
        logging.debug('Loading providers.')
        for provider in providers:
            logging.debug('Adding provider type - %s', provider)
            clouds = self.config.clouds(provider)
            try:
                provider_module = __import__("libcloud.%s.providers" % provider,
                                             fromlist=['libcloud'])
            except ImportError as ime:
                logging.error(ime)

            provider_factory = provider_module.get_driver

            for cloud in clouds:
                logging.debug('Adding driver type - %s.%s', provider, cloud)

                cls = provider_factory(cloud)
                self.api.add_resource(DriverResource,
                                      '/%s/clouds/%s' % (provider,
                                                         cloud),
                                      endpoint='%s_%s' % (provider,
                                                          cloud))
                for func in dir(cls):
                    if func[0] != '_':
                        if callable(getattr(cls, func)):
                            address = name_url(provider, cloud, func)
                            logging.debug('Added %s - %s', address[0], address[1])
