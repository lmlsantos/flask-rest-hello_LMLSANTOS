from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)
    favorite_characters = db.relationship('FavoriteCharacter', backref='user')
    favorite_planets = db.relationship('FavoritePlanet', backref='user')

    def __repr__(self):
        return '<User %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }
    
    class Character(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        name = db.Column(db.String(120), unique=True, nullable=False)
        gender = db.Column(db.String(120), unique=False, nullable=False)
        height = db.Column(db.String(80), unique=False, nullable=False)
        mass = db.Column(db.Integer, unique=False, nullable=False)
        hair_color = db.Column(db.String(80), unique=False, nullable=False)
        eye_color = db.Column(db.String(80), unique=False, nullable=False)
        birth_year = db.Column(db.Integer, unique=False, nullable=False)
        favorite_character = db.relationship('FavoriteCharacter', backref='character')

        def __repr__(self):
            return '<Character %r>' % self.id
        
        def serialize(self):
            return {
                "id": self.id,
                "name": self.name,
                "height": self.height,
                "mass":self.mass,
                "hair_color":self.hair_color,
                "eye_color": self.eye_color,
                "birth_year":self.hair_color
            }
        
    class Planet(db.Model):
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
        favorite_planet = db.relationship('FavoritePlanet', backref='planet')

        def __repr__(self):
            return '<Planet %r>' % self.id
        
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
        
    class Vehicle(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        name = db.Column(db.String(120), unique=True, nullable=False)
        model = db.Column(db.String(120), unique=False, nullable=False)
        crew = db.Columnn(db.Integer, unique=False, nullable=False)
        manufacurer = db.Column(db.String(120), unique=False, nullable=False)
        vehicle_class = db.Column(db.String(120), unique=False, nullable=False)
        length = db.Column(db.String(120), unique=False, nullable=False)

        def __repr__(self):
            return '<Vehicle %r>' % self.id
        
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
    
    class FavoriteCharacter(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        user_id =  db.Column(db.Integer, db.ForeignKey ('user.id'))
        character_id =  db.Column(db.Integer, db.ForeignKey ('character.id'))

        def serialize(self):
            return {
                "id": self.id,
                "user_id": self.user_id,
                "character_id": self.character_id,
        }

    
    class FavoritePlanet(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        user_id =  db.Column(db.Integer, db.ForeignKey ('user.id'))
        planet_id =  db.Column(db.Integer, db.ForeignKey ('planet.id'))

        def serialize(self):
            return {
                "id": self.id,
                "user_id": self.user_id,
                "planet_id": self.planet_id,
        }