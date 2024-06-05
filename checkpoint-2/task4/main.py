from wsgiref.simple_server import make_server

class InvertMiddleware:
    def __init__(self, application):
        self.app = application

    def __call__(self, environ, start_response, *args, **kwargs):
        response = self.app(environ, start_response)
        return [content[::-1] for content in response]

def simple_app(environ, start_response):
    body_content = [
        f'{key}: {value}' for key, value in sorted(environ.items())
    ]
    body_content = '\n'.join(body_content)

    status = '200 OK'
    headers = [('Content-type', 'text/plain')]

    start_response(status, headers)

    return [body_content.encode('utf-8')]

server = make_server('localhost', 8000, app=InvertMiddleware(simple_app))
server.serve_forever()
