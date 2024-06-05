from wsgiref.simple_server import make_server

class Reverseware:
    def __init__(self, app):
        self.wrapped_app = app

    def __call__(self, environ, start_response, *args, **kwargs):
        original_response = self.wrapped_app(environ, start_response)
        reversed_response = [data[::-1] for data in original_response]
        return reversed_response

def application(environ, start_response):
    response_body = '\n'.join(f'{key}: {value}' for key, value in sorted(environ.items()))
    status = '200 OK'
    response_headers = [('Content-type', 'text/plain')]
    start_response(status, response_headers)
    return [response_body.encode('utf-8')]

server = make_server('localhost', 8000, app=Reverseware(application))
server.serve_forever()
