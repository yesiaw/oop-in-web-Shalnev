import os
from pathlib import Path
import inspect

from parse import parse
from webob import Request, Response
from requests import Session as RequestsSession
from wsgiadapter import WSGIAdapter as RequestsWSGIAdapter
from jinja2 import Environment, FileSystemLoader
from whitenoise import WhiteNoise

from middleware import Middleware

class API:
    def __init__(self, templates_dir="templates", static_dir="static"):
        self.routes = {}
        self.templates_env = Environment(loader=FileSystemLoader(Path(templates_dir).resolve()))
        self.exception_handler = None
        self.whitenoise = WhiteNoise(self.wsgi_app, root=Path(static_dir).resolve())
        self.middleware = Middleware(self)

    def __call__(self, environ, start_response):
        path_info = environ["PATH_INFO"]
        if path_info.startswith("/static"):
            return self.whitenoise(dict(environ, PATH_INFO=path_info[7:]), start_response)
        return self.middleware(environ, start_response)

    def wsgi_app(self, environ, start_response):
        request = Request(environ)
        response = self.handle_request(request)
        return response(environ, start_response)

    def add_route(self, path, handler):
        assert path not in self.routes, "Such route already exists."
        self.routes[path] = handler

    def route(self, path):
        return lambda handler: self.add_route(path, handler) or handler

    def default_response(self, response):
        response.status_code = 404
        response.text = "Not found."

    def find_handler(self, request_path):
        for path, handler in self.routes.items():
            parse_result = parse(path, request_path)
            if parse_result:
                return handler, parse_result.named
        return None, None

    def handle_request(self, request):
        response = Response()
        handler, kwargs = self.find_handler(request_path=request.path)
        try:
            if handler:
                if inspect.isclass(handler):
                    handler = getattr(handler(), request.method.lower(), self.default_response)
                handler(request, response, **kwargs)
            else:
                self.default_response(response)
        except Exception as e:
            if self.exception_handler:
                self.exception_handler(request, response, e)
            else:
                raise
        return response

    def test_session(self, base_url="http://testserver"):
        session = RequestsSession()
        session.mount(base_url, RequestsWSGIAdapter(self))
        return session

    def template(self, template_name, context=None):
        return self.templates_env.get_template(template_name).render(context or {})

    def add_exception_handler(self, exception_handler):
        self.exception_handler = exception_handler

    def add_middleware(self, middleware_cls):
        self.middleware.add(middleware_cls)
