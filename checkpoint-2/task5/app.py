from api import API

app = API()

routes = [
    ("/home", "Hello from the HOME page"),
    ("/about", "Hello from the ABOUT page"),
    ("/sample", "sample")
]

for path, text in routes:
    @app.route(path)
    def generated_route(request, response, text=text):
        response.text = text

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
    def get(self, req, resp):
        resp.text = "Books Page"

    def post(self, req, resp):
        resp.text = "Endpoint to create a book"

@app.route("/template")
def template_handler(req, resp):
    resp.body = app.template("index.html", {"name": "Bumbo", "title": "Best Framework"}).encode()
