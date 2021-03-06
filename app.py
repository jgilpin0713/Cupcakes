"""Flask app for Cupcakes"""
from flask import Flask, request, redirect, render_template, jsonify
from models import db, connect_db, Cupcake

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)

def serialize_cupcake(cupcakes):
    """Serialize a cupcake SQLAlchemy obj to dictionary."""

    return {
        "id": cupcakes.id,
        "flavor": cupcakes.flavor,
        "size": cupcakes.size,
        "rating": cupcakes.rating,
        "image": cupcakes.image
    }

@app.route('/')
def index_page():
    """Renders HTML template that includes som JS"""
    cupcakes = Cupcake.query.all()
    return render_template("index.html", cupcakes = cupcakes)

@app.route("/api/cupcakes")
def get_all_cupcakes():
    """Return JSON about all cupcakes {cupcakes: [{id, flavor, size, rating, image}, ...]}"""
    all_cupcakes = [cupcake.serialize_cupcake() for cupcake in Cupcake.query.all()]

    return jsonify(cupcakes = all_todos)


@app.route("/api/cupcakes/<int:id>")
def single_cupcake(id):
    """Return JSON about a single cupcake cupcake: {id, flavor, size, rating, image}"""

    cupcake = Cupcake.query.get_or_404(id)

    return jsonify(cupcake = cupcake.serialized_cupcake())

@app.route("/api/cupcakes", methods =["POST"])
def create_cupcake():
    """Create a cupcake with flavor, size, rating and image 
    with JSON of {cupcake: {id, flavor, size, rating, image}}"""

    flavor = request.json["flavor"]
    size = request.json["size"]
    rating = request.json["rating"]
    image = request.json["image"]

    new_cupcake = Cupcake(flavor = flavor, size = size, rating = rating, image = image)

    db.session.add(new_cupcake)
    db.session.commit()

    serialized = serialize_cupcake(new_cupcake)

    return (jsonify(cupcake=serialized), 201)

@app.route("/api/cupcakes/<int:id>", methods=["PATCH"])
def update_cupcake(id):
    """Updates a particular cupcake and response with JSON to update that cupcake"""
    cupcake = Cupcake.query.get_or_404(id)
    cupcake.flavor = request.json.get("flavor", cupcake.flavor)
    cupcake.size = request.json.get("size", cupcake.size)
    cupcake.rating = request.json.get("rating", cupcake.rating)
    cupcake.image = request.json.get("image", cupcake.image)
    db.session.commit()
    return jsonify(cupcake=cupcake.serialize_cupcake())

@app.route("/api/cupcakes/<int:id>", methods = ["DELETE"])
def delete_cupcake(id):
    """ Deletes a particular cupcake"""
    cupcake = Cupcake.query.get_or_404(id)
    db.session.delete(cupcake)
    db.session.commit()
    return jsonify(message="Deleted")
