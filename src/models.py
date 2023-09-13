from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

db = SQLAlchemy()

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)
    
    def __repr__(self):
        return '<Users %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
             # do not serialize the password, its a security breach
        }
    
    class Characters(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        name = db.Column(db.String(120), unique=True, nullable=False)
        gender = db.Column(db.String(120), unique=False, nullable=False)
        height = db.Column(db.String(80), unique=False, nullable=False)
        mass = db.Column(db.Integer, unique=False, nullable=False)
        hair_color = db.Column(db.String(80), unique=False, nullable=False)
        eye_color = db.Column(db.String(80), unique=False, nullable=False)
        birth_year = db.Column(db.Integer, unique=False, nullable=False)
       
        def __repr__(self):
            return '<Characters %r>' % self.name
        
        def serialize(self):
            return {
                "id": self.id,
                "name": self.name,
                "height": self.height,
                "mass": self.mass,
                "hair_color":self.hair_color,
                "eye_color": self.eye_color,
                "birth_year":self.hair_color
            }
        
    class Planets(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        name = db.Column(db.String(120), unique=True, nullable=False)
        diameter = db.Columnn(db.Integer, unique=False, nullable=False)
        population = db.Column(db.Integer, unique=False, nullable=False)
        rotation_period = db.Column(db.Integer, unique=False, nullable=False)
        orbital_period = db.Column(db.Integer, unique=False, nullable=False)
        gravity = db.Column(db.Integer, unique=False, nullable=False)
        climate = db.Column(db.String(120), unique=True, nullable=False)
        population = db.Column(db.Integer, unique=False, nullable=False)
        terrain = db.Column(db.String(120), unique=False, nullable=False)
       
        def __repr__(self):
            return '<Planets %r>' % self.name
        
        def serialize(self):
            return {
                "id": self.id,
                "name": self.name,
                "diameter": self.diameter,
                "population": self.population,
                "rotation_period": self.rotation_period,
                "orbital_period": self.orbital_period,
                "gravity": self.gravity,
                "climate": self.climate,
                "population": self.population,
                "terrain": self.terrain
            }
        
    class Vehicles(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        name = db.Column(db.String(120), unique=True, nullable=False)
        model = db.Column(db.String(120), unique=False, nullable=False)
        crew = db.Columnn(db.Integer, unique=False, nullable=False)
        manufacurer = db.Column(db.String(120), unique=False, nullable=False)
        vehicle_class = db.Column(db.String(120), unique=False, nullable=False)
        length = db.Column(db.String(120), unique=False, nullable=False)

        def __repr__(self):
            return '<Vehicles %r>' % self.name
        
        def serialize(self):
            return {
                "id": self.id,
                "name": self.name,
                "model": self.model,
                "crew": self.crew,
                "manufacturer": self.manufacturer,
                "vehicle_class": self.vehicle_class,
                "length": self.length
            }
    
    class Favorites(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        users_id =  db.Column(db.Integer, db.ForeignKey ('users.id'))
        users = relationship('Users')
        characters_id =  db.Column(db.Integer, db.ForeignKey ('characters.id'))
        characters = relationship('Characters')
        planets_id =  db.Column(db.Integer, db.ForeignKey ('planets.id'))
        planets = relationship('Planets')
        vehicles_id =  db.Column(db.Integer, db.ForeignKey ('vehicles.id'))
        vehicles = relationship('Vehicles')

        def __repr__(self):
            return '<Favorites %r>' % self.id

        def serialize(self):
            return {
                "id": self.id,
                "Users": self.users.serialize(),
                "Characters": self.characters.serialize(),
                "planets": self.planets.serialize(),
                "vehicles": self.vehicles.serialize()
        }

    
    