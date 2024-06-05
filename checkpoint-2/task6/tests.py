import pytest
from api import API

@pytest.fixture
def api():
    return API()

@pytest.fixture
def client(api):
    return api.test_session()

def test_basic_route_adding(api):
    @api.route("/home")
    def home(req, resp):
        resp.text = "YOLO"

def test_route_overlap_throws_exception(api):
    @api.route("/home")
    def home(req, resp):
        resp.text = "YOLO"

    with pytest.raises(AssertionError):
        @api.route("/home")
        def home2(req, resp):
            resp.text = "YOLO"

def test_bumbo_test_client_can_send_requests(api, client):
    @api.route("/hey")
    def cool(req, resp):
        resp.text = "THIS IS COOL"

    assert client.get("http://testserver/hey").text == "THIS IS COOL"

def test_parameterized_route(api, client):
    @api.route("/{name}")
    def hello(req, resp, name):
        resp.text = f"hey {name}"

    assert client.get("http://testserver/matthew").text == "hey matthew"
    assert client.get("http://testserver/ashley").text == "hey ashley"

def test_default_404_response(client):
    response = client.get("http://testserver/doesnotexist")
    assert response.status_code == 404
    assert response.text == "Not found."

def test_class_based_handler_get(api, client):
    @api.route("/book")
    class BookResource:
        def get(self, req, resp):
            resp.text = "this is a get request"

    assert client.get("http://testserver/book").text == "this is a get request"

def test_class_based_handler_post(api, client):
    @api.route("/book")
    class BookResource:
        def post(self, req, resp):
            resp.text = "this is a post request"

    assert client.post("http://testserver/book").text == "this is a post request"

def test_class_based_handler_not_allowed_method(api, client):
    @api.route("/book")
    class BookResource:
        def post(self, req, resp):
            resp.text = "yolo"

    with pytest.raises(AttributeError):
        client.get("http://testserver/book")

def test_alternative_route(api, client):
    def home(req, resp):
        resp.text = "Alternative way to add a route"
    api.add_route("/alternative", home)
    assert client.get("http://testserver/alternative").text == "Alternative way to add a route"

def test_template(api, client):
    @api.route("/html")
    def html_handler(req, resp):
        resp.body = api.template("index.html", context={"title": "Some Title", "name": "Some Name"}).encode()
    response = client.get("http://testserver/html")
    assert "text/html" in response.headers["Content-Type"]
    assert "Some Title" in response.text
    assert "Some Name" in response.text

def test_custom_exception_handler(api, client):
    def on_exception(req, resp, exc):
        resp.text = "AttributeErrorHappened"
    api.add_exception_handler(on_exception)
    @api.route("/")
    def index(req, resp):
        raise AttributeError()
    response = client.get("http://testserver/")
    assert response.text == "AttributeErrorHappened"

def test_404_is_returned_for_nonexistent_static_file(client):
    assert client.get(f"http://testserver/{FILE_NAME}").status_code == 404
