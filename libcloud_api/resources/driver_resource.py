from flask_restful import Resource
from flask_restful import reqparse
from .parsers import ResultSets

__all__ = ['DriverResource']


class DriverResource(Resource):
    """
    Maps a driver to an API
    """

    def __init__(self, config, cloud, provider, cls, func, method, params):
        self.cls = cls
        self.func = func
        self.provider = provider
        self.config = config.get_cloud_args(provider, cloud)
        self.method = method
        self.params = params

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
        if self.method != 'GET':
            return Exception('Invalid request type')
        parser = reqparse.RequestParser()
        for arg in self.params.args:
            if arg != 'self':
                parser.add_argument(arg)

        # TODO : Cache instances
        args = parser.parse_args()
        result = getattr(self.instance, self.func)(*args)
        return self.parser.formatter(result)

    def post(self):
        if self.method != 'POST':
            return Exception('Invalid request type')
        # TODO : Cache instances
        result = getattr(self.instance, self.func)()
        return self.parser.formatter(result)

    def put(self):
        if self.method != 'PUT':
            return Exception('Invalid request type')
        # TODO : Cache instances
        result = getattr(self.instance, self.func)()
        return self.parser.formatter(result)

    def delete(self):
        if self.method != 'DELETE':
            return Exception('Invalid request type')
        # TODO : Cache instances
        result = getattr(self.instance, self.func)()
        return self.parser.formatter(result)