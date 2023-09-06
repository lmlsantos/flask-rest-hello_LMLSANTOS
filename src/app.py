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
from models import db, User, Character, Planet, Vehicle, FavoriteCharacter, FavoritePlanet
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
    users = User.query.all()
    serialize_users = [user.serialize() for user in users]

    response_body = {
        "msg": "This is the list of users",
        "result": serialize_users
    }

    return jsonify(response_body), 200

# GET ALL CHARACTERS
#------------------------------------------------------------
#------------------------------------------------------------
@app.route('/characters', methods=['GET'])
def get_characters(): 
    characters = Character.query.all()
    serialize_characters = [character.serialize() for character in characters]

    response_body = {
        "msg": "This is the list of characters",
        "result": serialize_characters
    }

    return jsonify(response_body), 200

# GET A PARTICULAR CHARACTER
#------------------------------------------------------------
@app.route('/characters/<int:id>', methods=['GET'])
def get_one_character(character_id):
    characters = Character.query.get(character_id)

    if characters is None:
        return jsonify({"msg": "Character doesnt exist"}), 404
    
    response_body = {
        "msg": "This is one character",
        "result": characters.serialize()
    }

    return jsonify(response_body), 200

# ADD A FAVORITE CHARACTER
#------------------------------------------------------------
@app.route('favorite/characters/<int:character_id>', methods=['POST'])
def create_favorite_character(character_id):
    new_favorite_character = FavoriteCharacter(user_id=1, character_id=character_id)
    db.session.add(new_favorite_character)
    db.session.commit()

    response_body = {
            "msg": "This is your post /favorite/characters/<int:character_id> response",
            "result": new_favorite_character.serialize()
        }
    return jsonify(response_body), 200

#DELETE A FAVORITE CHARACTER
#--------------------------------------------------------------
@app.route('favorite/characters/<int: id>', methods=['DELETE'])
def delete_favorite_character(character_id):
    favorite_character = FavoriteCharacter.query.get(character_id)
    db.session.delete(favorite_character)
    db.session.commit()

    response_body = {
        "msg": "This is your delete /favorite/characters/<int:id> response",
        "result": "Character Deleted"
    }
    return jsonify(response_body), 200



# GET ALL PLANETS
#------------------------------------------------------------
#------------------------------------------------------------
@app.route('/planets', methods=['GET'])
def get_planets():
    planets = Planet.query.all()
    serialize_planets = [planet.serialize() for planet in planets]

    response_body = {
        "msg": "This is the list of planets",
        "result": serialize_planets
    }

    return jsonify(response_body), 200

# GET A PARTICULAR PLANET
#------------------------------------------------------------
@app.route('planets/<int:id>', methods=['GET'])
def get_one_planet(planet_id):
    planets = Planet.query.get(planet_id)

    if planets is None:
        return jsonify({"msg": "Planet doesnt exist"}), 404
    
    response_body = {
        "msg": "This is one planet",
        "result": planets.serialize()
    }

    return jsonify(response_body), 200

# ADD A FAVORITE PLANET
#------------------------------------------------------------
@app.route('favorite/planets/<int:planet_id>', methods=['POST'])
def create_favorite_planet(planet_id):
    new_favorite_planet = FavoritePlanet(user_id=1, planet_id=planet_id)
    db.session.add(new_favorite_planet)
    db.session.commit()

    response_body = {
            "msg": "This is your post /favorite/planets/<int:planet_id> response",
            "result": new_favorite_planet.serialize()
        }
    return jsonify(response_body), 200

#DELETE A FAVORITE PLANET
#--------------------------------------------------------------
@app.route('favorite/planets/<int: id>', methods=['DELETE'])
def delete_favorite_planet(planet_id):
    favorite_planet = FavoritePlanet.query.get(planet_id)
    db.session.delete(favorite_planet)
    db.session.commit()

    response_body = {
        "msg": "This is your delete /favorite/planets/<int:id> response",
        "result": "Planet Deleted"
    }
    return jsonify(response_body), 200



# GET ALL VEHICLES
#------------------------------------------------------------
#------------------------------------------------------------
@app.route('/vehicles', methods=['GET'])
def get_vehicles():
    vehicles = Vehicle.query.all()
    serialize_vehicles = [vehicle.serialize() for vehicle in vehicles]

    response_body = {
        "msg": "This is the list of vehicles",
        "result": serialize_vehicles
    }

    return jsonify(response_body), 200

# GET A PARTICULAR VEHICLE
#------------------------------------------------------------
@app.route('vehicles/<int:id>', methods=['GET'])
def get_one_vehicle(vehicle_id):
    vehicles = Vehicle.query.get(vehicle_id)

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
    user_id = 1  
    fav_characters = db.session.query(Character).join(FavoriteCharacter).filter(FavoriteCharacter.user_id == user_id).all()
    fav_characters = [character.serialize() for character in fav_characters]
    fav_planets = []
    favorites = fav_characters + fav_planets

    response_body = {
        "msg": "This is the list of favorites for the user",
        "results": favorites
    }

    return jsonify(response_body), 200



# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
