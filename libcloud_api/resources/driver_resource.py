from flask_restful import Resource
from .parsers import ResultSets

__all__ = ['DriverResource']


class DriverResource(Resource):
    """
    Maps a driver to an API
    """

    def __init__(self, config, cloud, provider, cls, func):
        self.cls = cls
        self.func = func
        self.provider = provider
        self.config = config.get_cloud_args(provider, cloud)

        driver_args = [
            self.config['api_key'],
            self.config['api_secret']
            ]
        driver_kwargs = {}

        if 'region' in self.config:
            driver_kwargs['region'] = self.config['region']

        if 'extra_kwargs' in self.config:
            assert isinstance(self.config['extra_kwargs'], dict)
            driver_kwargs.update(self.config['extra_kwargs'])

        driver = cls(*driver_args, **driver_kwargs)
        self.instance = driver
        self.parser = ResultSets()

    def get(self):
        # TODO : Cache instances
        result = getattr(self.instance, self.func)()
        return self.parser.formatter(result)
