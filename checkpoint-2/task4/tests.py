import pytest
from web_framework import WebFramework as API

def test_adding_basic_route(create_api):
    @create_api.add_route("/home")
    def home(req, resp):
        resp.text = "Welcome Home"

def test_duplicate_route_raises_error(create_api):
    @create_api.add_route("/home")
    def home(req, resp):
        resp.text = "Welcome Home"

    with pytest.raises(AssertionError):
        @create_api.add_route("/home")
        def home2(req, resp):
            resp.text = "Home already exists"

def test_client_can_make_requests(create_api, create_client):
    MESSAGE = "Request received successfully"

    @create_api.add_route("/greet")
    def greet(req, resp):
        resp.text = MESSAGE

    assert create_client.get("http://testserver/greet").text == MESSAGE

def test_dynamic_routes(create_api, create_client):
    @create_api.add_route("/{username}")
    def greet_user(req, resp, username):
        resp.text = f"Hello, {username}"

    assert create_client.get("http://testserver/john").text == "Hello, john"
    assert create_client.get("http://testserver/jane").text == "Hello, jane"

def test_404_response(create_client):
    response = create_client.get("http://testserver/unknown")

    assert response.status_code == 404
    assert response.text == "Page not found."

def test_get_method_in_class_handler(create_api, create_client):
    GET_MESSAGE = "Handling GET request"

    @create_api.add_route("/library")
    class LibraryResource:
        def get(self, req, resp):
            resp.text = GET_MESSAGE

    assert create_client.get("http://testserver/library").text == GET_MESSAGE

def test_post_method_in_class_handler(create_api, create_client):
    POST_MESSAGE = "Handling POST request"

    @create_api.add_route("/library")
    class LibraryResource:
        def post(self, req, resp):
            resp.text = POST_MESSAGE

    assert create_client.post("http://testserver/library").text == POST_MESSAGE

def test_method_not_allowed_in_class_handler(create_api, create_client):
    @create_api.add_route("/library")
    class LibraryResource:
        def post(self, req, resp):
            resp.text = "Method allowed"

    with pytest.raises(AttributeError):
        create_client.get("http://testserver/library")
