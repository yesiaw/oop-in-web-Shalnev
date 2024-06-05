from web_framework import WebFramework as API

app = API()

@app.add_route("/home")
def home(req, resp):
    resp.text = "Welcome to the homepage!"

@app.add_route("/about")
def about(req, resp):
    resp.text = "Learn more about us on this page."

@app.add_route("/hello/{name}")
def greet_user(req, resp, name):
    resp.text = f"Greetings, {name}!"

@app.add_route("/tell/{age:d}")
def tell_age(req, resp, age):
    resp.text = f"Your age is {age} years."

@app.add_route("/sum/{num_1:d}/{num_2:d}")
def calculate_sum(req, resp, num_1, num_2):
    result = num_1 + num_2
    resp.text = f"The total of {num_1} and {num_2} is {result}."

@app.add_route("/book")
class BookResource:
    def get(self, req, resp):
        resp.text = "Welcome to the Books Resource page."

    def post(self, req, resp):
        resp.text = "Create a new book entry."

if __name__ == "__main__":
    from wsgiref.simple_server import make_server
    server = make_server('localhost', 8000, app)
    server.serve_forever()
