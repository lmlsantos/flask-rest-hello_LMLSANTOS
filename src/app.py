"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, Users, Characters, Planets, Vehicles, Favorites
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

# ENDPOINTS
# GET ALL USERS
#------------------------------------------------------------
#------------------------------------------------------------

@app.route('/users', methods=['GET'])
def get_all_users():
    
    all_users = Users.query.all()
    serialize_users = [user.serialize() for user in all_users]

    response_body = {
        "msg": "This is the list of users",
        "result": serialize_users
    }

    return jsonify(response_body), 200

# GET ALL CHARACTERS
#------------------------------------------------------------
#------------------------------------------------------------
@app.route('/characters', methods=['GET'])
def get_all_characters(): 
    
    all_characters = Characters.query.all()
    serialize_characters = [character.serialize() for character in all_characters]

    response_body = {
        "msg": "This is the list of characters",
        "result": serialize_characters
    }

    return jsonify(response_body), 200

# GET A PARTICULAR CHARACTER
#------------------------------------------------------------
@app.route('/characters/<int:character_id>', methods=['GET'])
def get_one_character(character_id):
    
    characters = Characters.query.get(character_id)

    if characters is None:
        return jsonify({"msg": "Character doesnt exist"}), 404
    
    response_body = {
        "msg": "This is one character",
        "result": characters.serialize()
    }

    return jsonify(response_body), 200

# GET ALL PLANETS
#------------------------------------------------------------
#------------------------------------------------------------
@app.route('/planets', methods=['GET'])
def get_all_planets():
    
    all_planets = Planets.query.all()
    serialize_planets = [planet.serialize() for planet in all_planets]

    response_body = {
        "msg": "This is the list of planets",
        "result": serialize_planets
    }

    return jsonify(response_body), 200

# GET A PARTICULAR PLANET
#------------------------------------------------------------
@app.route('planets/<int:planet_id>', methods=['GET'])
def get_one_planet(planet_id):
    
    planets = Planets.query.get(planet_id)

    if planets is None:
        return jsonify({"msg": "Planet doesnt exist"}), 404
    
    response_body = {
        "msg": "This is one planet",
        "result": planets.serialize()
    }

    return jsonify(response_body), 200

# GET ALL VEHICLES
#------------------------------------------------------------
#------------------------------------------------------------
@app.route('/vehicles', methods=['GET'])
def get_vehicles():
    
    all_vehicles = Vehicles.query.all()
    serialize_vehicles = [vehicle.serialize() for vehicle in all_vehicles]

    response_body = {
        "msg": "This is the list of vehicles",
        "result": serialize_vehicles
    }

    return jsonify(response_body), 200

# GET A PARTICULAR VEHICLE
#------------------------------------------------------------
@app.route('vehicles/<int:vehicle_id>', methods=['GET'])
def get_one_vehicle(vehicle_id):
    
    vehicles = Vehicles.query.get(vehicle_id)

    if vehicles is None:
        return jsonify({"msg": "Vehicle doesnt exist"}), 404
    
    response_body = {
        "msg": "This is one vehicle",
        "result": vehicles.serialize()
    }

    return jsonify(response_body), 200

# FAVORITES
#------------------------------------------------------------
@app.route('/users/favorites', methods=['GET'])
def get_user_favorites():
    
    all_favorites = Favorites.query.all()
    serialize_favorites = [favorite.serialize() for favorite in all_favorites]

    response_body = {
        "msg": "This is the list of favorites for the user",
        "results": serialize_favorites
    }

    return jsonify(response_body), 200

# ADD A FAVORITE
#------------------------------------------------------------
@app.route('/users/favorites', methods=['POST'])
def add_favorite_character():
    
    data = request.get_json()

    add_favorite = Favorites(
        character_id = data.get("character_id"),
        planet_id = data.get("planet_id"),
        vehicle_id = data.get("vehicle_id"),
        users_id = data.get("users_id")
    )

    db.session.add(add_favorite)
    db.session.commit()

    response_body = {
            "msg": "This is your post of favorites",
            "result": add_favorite.serialize()
    }

    return jsonify(response_body), 200

# UPDATE A FAVORITE
#------------------------------------------------------------
@app.route('/users/favorites/<int:id>', methods=['PUT'])
def update_favorite(id):

    favorite = Favorites.query.get(id)

    if not favorite:
        return jsonify({"message": "favorite not found"}), 404
    
    data = request.get_json()

    if "character_id" in data:
        favorite.character_id = data.get("character_id")

    if "planet_id" in data:
        favorite.planet_id = data.get("planet_id")

    if "vehicle_id" in data:
        favorite.vehicle_id = data.get("vehicle_id")

    if "users_id" in data:
        favorite.users_id = data.get("users_id")
 
    db.session.commit()
    
    return jsonify(favorite.serialize()), 200

#DELETE A FAVORITE PLANET
#--------------------------------------------------------------
@app.route('/users/favorites/<int:id>', methods=['DELETE'])
def delete_favorite(id):
    
    favorite = Favorites.query.get(id)

    if not favorite:
        return jsonify({"message": "favorite not found"}), 404
    
    db.session.delete(favorite)
    db.session.commit()
   
    response_body = {
            "msg": "Favorite Deleted",
    }

    return jsonify(response_body), 200


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
