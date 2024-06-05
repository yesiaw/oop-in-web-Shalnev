import inspect
from parse import parse
from webob import Request, Response
from requests import Session as RequestsSession
from wsgiadapter import WSGIAdapter as RequestsWSGIAdapter

class WebFramework:
    def __init__(self):
        self.route_handlers = {}

    def __call__(self, environ, start_response):
        req = Request(environ)
        resp = self.process_request(req)
        return resp(environ, start_response)

    def add_route(self, path):
        assert path not in self.route_handlers, "Route already exists."

        def wrapper(func):
            self.route_handlers[path] = func
            return func

        return wrapper

    def handle_404(self, resp):
        resp.status_code = 404
        resp.text = "Page not found."

    def get_handler(self, path):
        for route, handler in self.route_handlers.items():
            result = parse(route, path)
            if result is not None:
                return handler, result.named
        return None, None

    def process_request(self, req):
        resp = Response()
        handler, params = self.get_handler(req.path)

        if handler:
            if inspect.isclass(handler):
                handler = getattr(handler(), req.method.lower(), None)
                if handler is None:
                    raise AttributeError(f"Method {req.method} not allowed.")
            handler(req, resp, **params)
        else:
            self.handle_404(resp)

        return resp

    def create_test_session(self, base_url="http://testserver"):
        test_session = RequestsSession()
        test_session.mount(prefix=base_url, adapter=RequestsWSGIAdapter(self))
        return test_session
