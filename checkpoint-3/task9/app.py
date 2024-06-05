from api import API
from middleware import Middleware

app = API()

@app.route("/home")
def home(req, resp):
    resp.text = "Hello from the HOME page"

@app.route("/about")
def about(req, resp):
    resp.text = "Hello from the ABOUT page"

@app.route("/hello/{name}")
def greeting(req, resp, name):
    resp.text = f"Hello, {name}"

@app.route("/tell/{age:d}")
def telling(req, resp, age):
    resp.text = f"I tell your age: {age}"

@app.route("/sum/{num_1:d}/{num_2:d}")
def sum(req, resp, num_1, num_2):
    total = num_1 + num_2
    resp.text = f"{num_1} + {num_2} = {total}"

@app.route("/exception")
def exception_throwing_handler(req, resp):
    raise AssertionError("This handler should not be used.")

@app.route("/template")
def template_handler(req, resp):
    resp.html = app.template("index.html", context={"name": "Bumbo", "title": "Best Framework"})

@app.route("/json")
def json_handler(req, resp):
    resp.json = {"name": "data", "type": "JSON"}

@app.route("/text")
def text_handler(req, resp):
    resp.text = "This is a simple text"

@app.route("/book")
class BooksResource:
    def get(self, req, resp):
        resp.text = "Books Page"
    def post(self, req, resp):
        resp.text = "Endpoint to create a book"

def handler(req, resp):
    resp.text = "sample"
app.add_route("/sample", handler)

def custom_exception_handler(req, resp, exception):
    resp.text = str(exception)
app.add_exception_handler(custom_exception_handler)

class SimpleCustomMiddleware(Middleware):
    def process_request(self, req):
        print("Processing request", req.url)
    def process_response(self, req, res):
        print("Processing response", req.url)
app.add_middleware(SimpleCustomMiddleware)
