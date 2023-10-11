"""Flask app for Cupcakes"""
from flask import Flask, request, jsonify, render_template
from models import *

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcake'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "secret159"

app.app_context().push()

connect_db(app)

@app.route('/')
def homepage():
    cupcake = Cupcake.query.all()
    return render_template('homepage.html', cupcake=cupcake)

@app.route('/api/cupcakes')
def get_cupcakes_data():
    """Get cupcakes data"""

    cupcakes = Cupcake.query.all()
    serialized = [Cupcake.serialize_cupcake(i) for i in cupcakes]
    return jsonify(cupcakes=serialized)

@app.route('/api/cupcakes/<int:cupcake_id>')
def get_cupcake_data(cupcake_id):
    """Get one cupcake data"""

    cupcake = Cupcake.query.get_or_404(cupcake_id)
    serialized = Cupcake.serialize_cupcake(cupcake)

    return jsonify(cupcake=serialized)

@app.route('/api/cupcakes', methods=['POST'])
def create_cupcake():
    """Create cupcake"""

    data = request.json

    cupcake = Cupcake(flavor=data['flavor'], size=data['size'], rating=data['rating'], image=data['image'])
    db.session.add(cupcake)
    db.session.commit()

    return jsonify(cupcake=cupcake.serialize_cupcake())

@app.route('/api/cupcakes/<int:cupcake_id>', methods=['PATCH'])
def update_cupcake(cupcake_id):

    data= request.json
    cupcake = Cupcake.query.get_or_404(cupcake_id)

    cupcake.flavor = data['flavor']
    cupcake.size = data['size']
    cupcake.rating = data['rating']
    cupcake.image = data['image']

    db.session.add(cupcake)
    db.session.commit()

    return jsonify(cupcake=cupcake.serialize_cupcake())

@app.route('/api/cupcakes/<int:cupcake_id>', methods=['DELETE'])
def delete_cupcake(cupcake_id):
    """delete cupcake"""

    data = request.json

    cupcake = Cupcake.query.get_or_404(cupcake_id)

    db.session.add(cupcake)
    db.session.commit()

    return jsonify("delete successful")

