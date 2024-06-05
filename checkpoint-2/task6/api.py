import inspect
import os
from parse import parse
from webob import Request, Response
from requests import Session as RequestsSession
from wsgiadapter import WSGIAdapter as RequestsWSGIAdapter
from jinja2 import Environment, FileSystemLoader
from whitenoise import WhiteNoise

class API:
    def __init__(self, templates_dir="templates"):
        self.routes = {}
        self.templates_env = Environment(loader=FileSystemLoader(os.path.abspath(templates_dir)))
        self.exception_handler = None
        self.whitenoise = WhiteNoise(self.wsgi_app, root=static_dir)

    def __call__(self, environ, start_response):
        return self.whitenoise(environ, start_response)

    def wsgi_app(self, environ, start_response):
        request = Request(environ)
        response = self.handle_request(request)
        return response(environ, start_response)

    def add_route(self, path, handler):
        assert path not in self.routes, "Such route already exists."
        self.routes[path] = handler

    def route(self, path):
        def wrapper(handler):
            self.add_route(path, handler)
            return handler
        return wrapper

    def default_response(self, response):
        response.status_code = 404
        response.text = "Not found."

    def find_handler(self, request_path):
        for path, handler in self.routes.items():
            parse_result = parse(path, request_path)
            if parse_result is not None:
                return handler, parse_result.named
        return None, None

    def handle_request(self, request):
        response = Response()
        try:
            handler, kwargs = self.find_handler(request_path=request.path)
            if handler:
                if inspect.isclass(handler):
                    handler = getattr(handler(), request.method.lower(), None)
                if handler:
                    handler(request, response, **kwargs)
                else:
                    raise AttributeError("Method not allowed", request.method)
            else:
                self.default_response(response)
        except Exception as e:
            if self.exception_handler:
                self.exception_handler(request, response, e)
            else:
                raise e
        return response

    def test_session(self, base_url="http://testserver"):
        session = RequestsSession()
        session.mount(base_url, RequestsWSGIAdapter(self))
        return session

    def template(self, template_name, context=None):
        if context is None:
            context = {}
        return self.templates_env.get_template(template_name).render(context)

    def add_exception_handler(self, exception_handler):
        self.exception_handler = exception_handler
