# -*- coding: utf-8 -*-
from yaml import load as yaml_load


class config(object):
    def __init__(self, config_file_name='config.yaml'):
        with open(config_file_name, "r") as config_stream:
            self.config = yaml_load(config_stream)

    def providers(self):
        """
        Get a list of configured providers (driver types)
        """
        return [item for item in self.config['providers']]

    def clouds(self, provider):
        """
        List the configured clouds (drivers)
        for a given provider
        """
        return [item for item in self.config['providers'][provider]['clouds']]