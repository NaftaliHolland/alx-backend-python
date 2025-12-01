import logging
from datetime import datetime

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.logger = logging.getLogger(__name__)
        logging.basicConfig(
            filename='requests.log',
            encoding='utf-8',
            level=logging.INFO,
            format='%(message)s'
        )

    def __call__(self, request):

        self.logger.info(f'{datetime.now()}-User:{request.user}-Path:{request.path}')

        response = self.get_response(request)
        return response
