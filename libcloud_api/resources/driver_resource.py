import logging
from flask_restful import Resource

__all__ = ['DriverResource']


class DriverResource(Resource):
    """
    Maps a driver to an API
    """

    def __init__(self, api, cls):
        self.api = api
        self.cls = cls

