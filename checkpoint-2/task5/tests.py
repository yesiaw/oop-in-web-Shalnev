import pytest
from api import API

def register_route(api, path, handler, method='get'):
    @api.route(path)
    class RouteResource:
        def __getattribute__(self, item):
            if item == method:
                return lambda req, resp: handler(req, resp)
            return super().__getattribute__(item)

@pytest.mark.parametrize("path, response_text", [
    ("/home", "YOLO"),
    ("/hey", "THIS IS COOL"),
    ("/matthew", "hey matthew"),
    ("/ashley", "hey ashley"),
    ("/alternative", "Alternative way to add a route")
])
def test_route_responses(api, client, path, response_text):
    def handler(req, resp):
        resp.text = response_text

    register_route(api, path, handler)
    assert client.get(f"http://testserver{path}").text == response_text

def test_route_overlap_throws_exception(api):
    register_route(api, "/home", lambda req, resp: resp.text = "YOLO")
    with pytest.raises(AssertionError):
        register_route(api, "/home", lambda req, resp: resp.text = "YOLO")

def test_default_404_response(client):
    response = client.get("http://testserver/doesnotexist")
    assert response.status_code == 404
    assert response.text == "Not found."

@pytest.mark.parametrize("method, expected_text", [
    ("get", "this is a get request"),
    ("post", "this is a post request")
])
def test_class_based_handlers(api, client, method, expected_text):
    def handler(req, resp):
        resp.text = expected_text

    register_route(api, "/book", handler, method)
    assert getattr(client, method)(f"http://testserver/book").text == expected_text

def test_class_based_handler_not_allowed_method(api, client):
    register_route(api, "/book", lambda req, resp: resp.text = "yolo", 'post')
    with pytest.raises(AttributeError):
        client.get("http://testserver/book")

def test_template(api, client):
    @api.route("/html")
    def html_handler(req, resp):
        resp.body = api.template("index.html", context={"title": "Some Title", "name": "Some Name"}).encode()

    response = client.get("http://testserver/html")
    assert "text/html" in response.headers["Content-Type"]
    assert "Some Title" in response.text
    assert "Some Name" in response.text
