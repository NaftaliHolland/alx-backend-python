import logging
from datetime import datetime, time

from django.http import HttpResponse


class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.logger = logging.getLogger(__name__)
        logging.basicConfig(
            filename="requests.log",
            encoding="utf-8",
            level=logging.INFO,
            format="%(message)s",
        )

    def __call__(self, request):

        self.logger.info(f"{datetime.now()}-User:{request.user}-Path:{request.path}")

        response = self.get_response(request)
        return response


class RestrictAccessByTimeMiddleware:

    def __init__(self, get_response):

        self.get_response = get_response

    def __call__(self, request):

        response = self.get_response(request)
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):

        now = datetime.now().time()

        print("Time now", now)

        start = time(18, 0)
        end = time(21, 0)

        is_between = start <= now <= end

        if is_between:
            return HttpResponse("You cannot access this app at this time", status=403)

        return None
