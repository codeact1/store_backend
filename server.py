from flask import Flask
import json
from config import me, hello
from mock_data import catalog
app = Flask("Server")


@app.get("/")
def home():
    return "Hello from Flask"


@app.get("/test")
def test():
    return "This is a test"


@app.get("/about")
def about():
    return "Chaka"


######################################################################################################
#    API END POINTS
#    JSON
######################################################################################################


@app.get("/api/version")
def version():
    v = {
        "version": "1.0",
        "build": 21,
        "name": "tiger",
        "developer": me
    }

    hello()
    return json.dumps(v)


@app.get("/api/catalog")
def get_catalog():
    return json.dumps(catalog)


@app.get("/api/products/count")
def get_count():
    return json.dumps(len(catalog))


app.run(debug=True)
