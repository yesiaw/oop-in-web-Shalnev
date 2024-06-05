import os
import inspect
from parse import parse
from webob import Request, Response
from requests import Session
from wsgiadapter import WSGIAdapter
from jinja2 import Environment, FileSystemLoader

class API:
    def __init__(self, templates_dir="templates"):
        self.routes = {}
        templates_path = os.path.abspath(templates_dir)
        self.templates_env = Environment(loader=FileSystemLoader(templates_path))

    def __call__(self, environ, start_response):
        request = Request(environ)
        response = self.handle_request(request)
        return response(environ, start_response)

    def add_route(self, path, handler):
        if path in self.routes:
            raise AssertionError("Such route already exists.")
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
            if parse_result := parse(path, request_path):
                return handler, parse_result.named
        return None, None

    def handle_request(self, request):
        response = Response()
        handler, kwargs = self.find_handler(request.path)

        if handler:
            self.execute_handler(handler, request, response, kwargs)
        else:
            self.default_response(response)
        return response

    def execute_handler(self, handler, request, response, kwargs):
        if inspect.isclass(handler):
            handler_instance = handler()
            handler_method = getattr(handler_instance, request.method.lower(), None)
            if not handler_method:
                raise AttributeError("Method not allowed", request.method)
            handler = handler_method
        handler(request, response, **kwargs)

    def test_session(self, base_url="http://testserver"):
        session = Session()
        session.mount(base_url, WSGIAdapter(self))
        return session

    def template(self, template_name, context=None):
        if not context:
            context = {}
        return self.templates_env.get_template(template_name).render(context)
