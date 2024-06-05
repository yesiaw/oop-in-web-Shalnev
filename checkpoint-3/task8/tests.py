import pytest

from api import API
from middleware import Middleware

def test_basic_route_adding(api):
    @api.route("/home")
    def home(request, response):
        response.text = "YOLO"

def test_route_overlap_throws_exception(api):
    @api.route("/home")
    def home1(request, response):
        response.text = "YOLO"

    with pytest.raises(AssertionError):
        @api.route("/home")
        def home2(request, response):
            response.text = "YOLO"

def test_request_to_specific_route(api, client):
    expected_text = "THIS IS COOL"

    @api.route("/hey")
    def response_handler(request, response):
        response.text = expected_text

    assert client.get("http://testserver/hey").text == expected_text

def test_dynamic_route_handling(api, client):
    @api.route("/{name}")
    def greet(request, response, name):
        response.text = f"hey {name}"

    assert client.get("http://testserver/matthew").text == "hey matthew"
    assert client.get("http://testserver/ashley").text == "hey ashley"

def test_non_existent_route_returns_404(client):
    response = client.get("http://testserver/doesnotexist")
    assert response.status_code == 404
    assert response.text == "Not found."

def test_get_request_via_class_based_handler(api, client):
    expected_response = "this is a get request"

    @api.route("/book")
    class BookResource:
        def get(self, request, response):
            response.text = expected_response

    assert client.get("http://testserver/book").text == expected_response

def test_post_request_via_class_based_handler(api, client):
    expected_response = "this is a post request"

    @api.route("/book")
    class BookResource:
        def post(self, request, response):
            response.text = expected_response

    assert client.post("http://testserver/book").text == expected_response

def test_unallowed_method_for_class_based_handler(api, client):
    @api.route("/book")
    class BookResource:
        def post(self, request, response):
            response.text = "yolo"

    with pytest.raises(AttributeError):
        client.get("http://testserver/book")

def test_alternative_way_to_add_route(api, client):
    message = "Alternative way to add a route"

    def alternative_route(request, response):
        response.text = message

    api.add_route("/alternative", alternative_route)
    assert client.get("http://testserver/alternative").text == message

def test_rendering_html_via_template(api, client):
    @api.route("/html")
    def html_route_handler(request, response):
        response.body = api.template("index.html", context={"title": "Some Title", "name": "Some Name"}).encode()

    response = client.get("http://testserver/html")
    assert "text/html" in response.headers["Content-Type"]
    assert "Some Title" in response.text
    assert "Some Name" in response.text

def test_handling_exceptions_via_custom_handler(api, client):
    def handle_exception(request, response, exception):
        response.text = "AttributeErrorHappened"

    api.add_exception_handler(handle_exception)

    @api.route("/")
    def raise_exception(request, response):
        raise AttributeError()

    response = client.get("http://testserver/")
    assert response.text == "AttributeErrorHappened"

def test_middleware_invocation(api, client):
    request_processed = False
    response_processed = False

    class TestMiddleware(Middleware):
        def __init__(self, app):
            super().__init__(app)

        def process_request(self, request):
            nonlocal request_processed
            request_processed = True

        def process_response(self, request, response):
            nonlocal response_processed
            response_processed = True

    api.add_middleware(TestMiddleware)

    @api.route('/')
    def index_route(request, response):
        response.text = "YOLO"

    client.get('http://testserver/')
    assert request_processed
    assert response_processed

def test_enforcing_allowed_methods(api, client):
    @api.route("/home", allowed_methods=["post"])
    def post_only_route(request, response):
        response.text = "Hello"

    with pytest.raises(AttributeError):
        client.get("http://testserver/home")

    assert client.post("http://testserver/home").text == "Hello"
