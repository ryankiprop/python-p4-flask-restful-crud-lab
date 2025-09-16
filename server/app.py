from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
from models import db, Plant
import os

app = Flask(__name__)

# Configure database URI based on environment
if os.environ.get('TESTING') == 'True':
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///plants.db'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False

CORS(app)
db.init_app(app)

@app.before_first_request
def create_tables():
    db.create_all()

@app.route('/')
def index():
    return '<h1>Plant Server</h1>'

# GET /plants route
@app.route('/plants', methods=['GET'])
def get_plants():
    plants = Plant.query.all()
    return jsonify([plant.to_dict() for plant in plants])

# GET /plants/:id route
@app.route('/plants/<int:id>', methods=['GET'])
def get_plant(id):
    plant = Plant.query.get(id)
    if plant:
        return jsonify(plant.to_dict())
    return make_response(jsonify({"error": "Plant not found"}), 404)

# PATCH /plants/:id route - Update plant
@app.route('/plants/<int:id>', methods=['PATCH'])
def update_plant(id):
    plant = Plant.query.get(id)
    if not plant:
        return make_response(jsonify({"error": "Plant not found"}), 404)
    
    data = request.get_json()
    if 'is_in_stock' in data:
        plant.is_in_stock = data['is_in_stock']
    
    db.session.commit()
    return jsonify(plant.to_dict())

# DELETE /plants/:id route - Delete plant
@app.route('/plants/<int:id>', methods=['DELETE'])
def delete_plant(id):
    plant = Plant.query.get(id)
    if not plant:
        return make_response(jsonify({"error": "Plant not found"}), 404)
    
    db.session.delete(plant)
    db.session.commit()
    return make_response('', 204)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(port=5555, debug=True)