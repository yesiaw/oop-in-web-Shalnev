from webob import Request, Response
from typing import Callable, Any

class Middleware:
    def __init__(self, app: Callable):
        self.app = app

    def __call__(self, environ: dict, start_response: Callable) -> Any:
        request = Request(environ)
        response = self.handle_request(request)
        return response(environ, start_response)

    def add(self, middleware_cls: type) -> None:
        self.app = middleware_cls(self.app)

    def process_request(self, req: Request) -> None:
        pass

    def process_response(self, req: Request, resp: Response) -> None:
        pass

    def handle_request(self, request: Request) -> Response:
        self.process_request(request)
        response = self.app.handle_request(request)
        self.process_response(request, response)
        return response

