from api import API

app = API()

@app.route("/home")
def home(request, response):
    response.text = "Hello from the HOME page"

@app.route("/about")
def about(request, response):
    response.text = "Hello from the ABOUT page"

@app.route("/hello/{name}")
def greeting(request, response, name):
    response.text = f"Hello, {name}"

@app.route("/tell/{age:d}")
def telling(request, response, age):
    response.text = f"I tell your age: {age}"

@app.route("/sum/{num_1:d}/{num_2:d}")
def sum(request, response, num_1, num_2):
    total = num_1 + num_2
    response.text = f"{num_1} + {num_2} = {total}"

@app.route("/book")
class BooksResource:
    def get(self, request, response):
        response.text = "Books Page"

    def post(self, request, response):
        response.text = "Endpoint to create a book"

@app.route("/template")
def template_handler(request, response):
    response.body = app.template("index.html", context={"name": "Bumbo", "title": "Best Framework"}).encode()

@app.route("/exception")
def exception_throwing_handler(request, response):
    raise AssertionError("This handler should not be used.")

def handler(request, response):
    response.text = "sample"

app.add_route("/sample", handler)

def custom_exception_handler(request, response, exception):
    response.text = str(exception)

app.add_exception_handler(custom_exception_handler)
