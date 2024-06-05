import json
from webob import Response as WebObResponse

class Response:
    def __init__(self):
        self.json = None
        self.html = None
        self.text = None
        self.content_type = None
        self.body = b''
        self.status_code = 200

    def __call__(self, environ, start_response):
        self.prepare_response_body()
        response = WebObResponse(body=self.body, content_type=self.content_type, status=self.status_code)
        return response(environ, start_response)

    def prepare_response_body(self):
        if self.json is not None:
            self.body = json.dumps(self.json).encode('utf-8')
            self.content_type = "application/json"
        elif self.html is not None:
            self.body = self.html.encode('utf-8')
            self.content_type = "text/html"
        elif self.text is not None:
            self.body = self.text.encode('utf-8')
            self.content_type = "text/plain"

