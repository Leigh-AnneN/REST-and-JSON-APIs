"""Flask app for Cupcakes"""

from flask import Flask,request, render_template, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, Cupcake

app = Flask(__name__)
app.app_context().push()

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "SECRET!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

@app.route("/")
def root():
    "Render Homepage"
    return render_template("index.html")

@app.route("/api/cupcakes")
def list_all_cupcakes():
    """Return all cupcakes in the system
    Return JSONlike:
        {cupcakes: [{id, flavor, size, rating, image}, ...]}.
        """
    all_cupcakes = [cupcake.serialize() for cupcake in Cupcake.query.all()]
    return jsonify (cupcakes = all_cupcakes)

@app.route("/api/cupcakes/<int:id>")
def get_cupcake(id):
    """Get data about a single cupcake."""
    cupcake = Cupcake.query.get_or_404(id)
    return jsonify (cupcake= cupcake.serialize())
    
@app.route("/api/cupcakes", methods=["POST"])
def create_cupcake():
    """Add cupcake, and return data about new cupcake.

    Returns JSON like:
        {cupcake: [{id, flavor, rating, size, image}]}
    """
    data = request.json
    new_cupcake = Cupcake(
        flavor=data["flavor"],
        rating= data["rating"],
        size = data["size"],
        image= data["image"] or None
    )
    
    db.session.add(new_cupcake)
    db.session.commit()

    return (jsonify(cupcake=new_cupcake.serialize()), 201)

@app.route('/api/cupcakes/<int:id>', methods=["PATCH"])
def update_cupcakes(id):
    """Update a cupcake with the id passed in the URL and flavor, size, rating and image data from the body of the request. You can always assume that the entire cupcake object will be passed to the backend."""
    cupcake = Cupcake.query.get_or_404(id)
    request.json
    cupcake.flavor=request.json.get('flavor',cupcake.flavor)
    cupcake.rating= request.json.get('rating', cupcake.rating)
    cupcake.size = request.json.get('size', cupcake.size)
    cupcake.image= request.json.get('image',cupcake.image)

    db.session.commit()
    return jsonify(cupcake=cupcake.serialize())

@app.route('/api/cupcakes/<int:id>', methods=["DELETE"])
def delete_cupcake(id):
    """Delete cupcake and return confirmation message.

    Returns JSON of {message: "Deleted"}
    """
    cupcake = Cupcake.query.get_or_404(id)
    db.session.delete(cupcake)
    db.session.commit()

    return jsonify(message="deleted")


connect_db(app)
db.create_all()

