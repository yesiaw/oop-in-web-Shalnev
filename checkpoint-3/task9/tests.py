import pytest
from api import API

def test_add_basic_route(api):
    @api.route("/home")
    def home(req, resp):
        resp.text = "Hello from home"

def test_duplicate_route_throws_exception(api):
    @api.route("/home")
    def home_first(req, resp):
        resp.text = "First home"

    with pytest.raises(AssertionError):
        @api.route("/home")
        def home_second(req, resp):
            resp.text = "Second home"

def test_client_request_handling(api, client):
    @api.route("/hello")
    def hello(req, resp):
        resp.text = "Hello, world!"

    assert client.get("http://testserver/hello").text == "Hello, world!"

def test_parameterized_routes(api, client):
    @api.route("/{name}")
    def greet(req, resp, name):
        resp.text = f"Hello, {name}!"

    assert client.get("http://testserver/Alice").text == "Hello, Alice!"
    assert client.get("http://testserver/Bob").text == "Hello, Bob!"

def test_default_404_response(client):
    response = client.get("http://testserver/nonexistent")
    assert response.status_code == 404
    assert response.text == "Not found."

def test_class_based_get_request(api, client):
    @api.route("/resource")
    class Resource:
        def get(self, req, resp):
            resp.text = "GET request handled"

    assert client.get("http://testserver/resource").text == "GET request handled"

def test_class_based_post_request(api, client):
    @api.route("/resource")
    class Resource:
        def post(self, req, resp):
            resp.text = "POST request handled"

    assert client.post("http://testserver/resource").text == "POST request handled"
    with pytest.raises(AttributeError):
        client.get("http://testserver/resource")

def test_custom_exception_handling(api, client):
    def handle_exception(req, resp, exc):
        resp.text = "Exception handled"

    api.add_exception_handler(handle_exception)
    @api.route("/")
    def raise_error(req, resp):
        raise Exception("Test exception")

    response = client.get("http://testserver/")
    assert response.text == "Exception handled"

def test_response_helpers(api, client):
    @api.route("/json")
    def json_response(req, resp):
        resp.json = {"message": "This is JSON"}

    @api.route("/html")
    def html_response(req, resp):
        resp.html = "<h1>This is HTML</h1>"

    @api.route("/text")
    def text_response(req, resp):
        resp.text = "This is plain text"

    json_resp = client.get("http://testserver/json")
    html_resp = client.get("http://testserver/html")
    text_resp = client.get("http://testserver/text")

    assert json_resp.json()["message"] == "This is JSON"
    assert "text/html" in html_resp.headers["Content-Type"]
    assert text_resp.text == "This is plain text"
