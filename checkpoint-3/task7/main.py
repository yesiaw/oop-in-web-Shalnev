from wsgiref.simple_server import make_server
from typing import Callable, List


class Reverseware:
    def __init__(self, app: Callable):
        self.wrapped_app = app

    def __call__(self, environ: dict, start_response: Callable) -> List[bytes]:
        wrapped_app_response = self.wrapped_app(environ, start_response)
        return [data[::-1] for data in wrapped_app_response]


def application(environ: dict, start_response: Callable) -> List[bytes]:
    response_body = [f'{key}: {value}' for key, value in sorted(environ.items())]
    response_body = '\n'.join(response_body)
    status = '200 OK'
    response_headers = [('Content-type', 'text/plain')]
    start_response(status, response_headers)
    return [response_body.encode('utf-8')]


if __name__ == '__main__':
    server = make_server('localhost', 8000, app=Reverseware(application))
    print("Serving HTTP on port 8000...")
    server.serve_forever()
