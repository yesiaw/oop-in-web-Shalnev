import os
import inspect
from parse import parse
from webob import Request, Response
from requests import Session as RequestsSession
from wsgiadapter import WSGIAdapter as RequestsWSGIAdapter
from jinja2 import Environment, FileSystemLoader
from whitenoise import WhiteNoise
from middleware import Middleware

class API:
    def __init__(self, templates_dir="templates"):
        self.routes = {}
        templates_path = os.path.abspath(templates_dir)
        self.templates_env = Environment(loader=FileSystemLoader(templates_path))
        self.exception_handler = None
        self.whitenoise = WhiteNoise(self.wsgi_app, root=static_dir)
        self.middleware = Middleware(self)

    def __call__(self, environ, start_response):
        path_info = environ["PATH_INFO"]
        return self.middleware(environ, start_response)

    def wsgi_app(self, environ, start_response):
        request = Request(environ)
        response = self.handle_request(request)
        return response(environ, start_response)

    def add_route(self, path, handler, allowed_methods=None):
        assert path not in self.routes, "Such route already exists."
        if allowed_methods is None:
            allowed_methods = ['GET', 'POST', 'PUT', 'PATCH', 'DELETE', 'OPTIONS']
        self.routes[path] = {"handler": handler, "allowed_methods": [method.lower() for method in allowed_methods]}

    def route(self, path, allowed_methods=None):
        def wrapper(handler):
            self.add_route(path, handler, allowed_methods)
            return handler
        return wrapper

    def default_response(self, response):
        response.status_code = 404
        response.text = "Not found."

    def find_handler(self, request_path):
        for path, handler_data in self.routes.items():
            parse_result = parse(path, request_path)
            if parse_result is not None:
                return handler_data, parse_result.named
        return None, None

    def handle_request(self, request):
        response = Response()
        handler_data, kwargs = self.find_handler(request_path=request.path)
        try:
            if handler_data:
                handler = handler_data["handler"]
                allowed_methods = handler_data["allowed_methods"]
                if inspect.isclass(handler):
                    handler = getattr(handler(), request.method.lower(), None)
                    if not handler:
                        raise AttributeError("Method not allowed", request.method)
                elif request.method.lower() not in allowed_methods:
                    raise AttributeError("Method not allowed", request.method)
                handler(request, response, **kwargs)
            else:
                self.default_response(response)
        except Exception as e:
            if not self.exception_handler:
                raise
            self.exception_handler(request, response, e)
        return response

    def test_session(self, base_url="http://testserver"):
        session = RequestsSession()
        session.mount(base_url, RequestsWSGIAdapter(self))
        return session

    def template(self, template_name, context=None):
        context = context or {}
        return self.templates_env.get_template(template_name).render(**context)

    def add_exception_handler(self, exception_handler):
        self.exception_handler = exception_handler

    def add_middleware(self, middleware_cls):
        self.middleware.add(middleware_cls)
