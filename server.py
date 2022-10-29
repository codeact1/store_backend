from flask import Flask, request, abort
import json
from config import me, db
from mock_data import catalog
from bson import ObjectId

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

    return json.dumps(v)


def fix_id(obj):
    obj["_id"] = str(obj["_id"])
    return obj


@app.get("/api/catalog")
def get_catalog():
    cursor = db.products.find({}).sort("title")
    results = []
    for prod in cursor:
        results.append(fix_id(prod))

    return json.dumps(results)


@app.post("/api/catalog")
def save_product():
    product = request.get_json()

    if product is None:
        return abort(400, "product required")

    product["category"] = "Category".lower()

    db.products.insert_one(product)

    product["_id"] = str(product["_id"])

    return json.dumps(product)


@app.put("/api/catalog")
def update_product():
    product = request.get_json()
    # id = product["_id"] #read it
    # del product["_id"] #delete it
    id = product.pop("_id")  # read and delete it

    res = db.products.update_one({"_id": ObjectId(id)}, {"$set": product})

    return json.dumps(res)


@app.delete("/api/catalog/<id>")
def delete_product(id):

    res = db.products.delete_one({"_id": ObjectId(id)})

    return json.dumps({"count": res.deleted_count})
    # del returning usable data{"deleted_count": 1}


@app.get("/api/products/count")
def get_count():
    count = db.products.count_documents({})
    return json.dumps(count)


@app.get("/api/products/total")
def total_price():
    total = 0
    # get the products from db into a cursor
    cursor = db.products.find({})

    # travel the cursor
    for prod in cursor:
        total += prod["price"]
    return json.dumps(total)


@app.get("/api/product/details/<id>")
def get_details(id):
    prod = db.products.find_one({"_id": ObjectId(id)})
    if prod:
        return json.dumps(fix_id(prod))

    return abort(404, "Product not found")


@app.get("/api/catalog/<category>")
def by_category(category):
    results = []
    cursor = db.products.find({"category": category})
    for prod in cursor:
        results.append(fix_id(prod))
    return json.dumps(results)


@app.get("/api/catalog/lower/<amount>")
def lower_than(amount):
    results = []
    cursor = db.products.find({"price": {"$lt": float(amount)}})
    for prod in cursor:
        if prod["price"] < float(amount):
            results.append(prod)

    return json.dumps(results)


@app.get("/api/catalog/higher/<amount>")
def greater_than(amount):
    results = []
    cursor = db.products.find({"price": {"$gte": float(amount)}})
    for prod in cursor:
        results.append(fix_id(prod))

    return json.dumps(results)


@app.get("/api/category/unique")
def unique_cat():
    results = []
    cursor = db.products.distinct("category")
    for cat in cursor:
        results.append(cat)

    return json.dumps(results)


@app.get("/api/test/colors")
def unique_colors():
    colors = ["red", 'blue', "Pink", "yelloW", "Red",
              "Black", "BLUE", "RED", "BLACK", "YELLOW"]
    results = []
    for color in colors:
        color = color.lower()
        if not color in results:
            results.append(colors)

        return json.dumps(results)


@app.get("/api/test/count/<color>")
def count_color(color):
    color = color.lower()
    colors = ["red", 'blue', "Pink", "yelloW", "Red",
              "Black", "BLUE", "RED", "BLACK", "YELLOW"]
    count = 0
    for item in colors:
        if color == item.lower():
            count += 1

        return json.dumps(count)


# app.run(debug=True)
