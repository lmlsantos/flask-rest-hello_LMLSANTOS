import os
from flask_admin import Admin
from models import db, User, Character, Planet, Vehicle, Favorites
from flask_admin.contrib.sqla import ModelView

def setup_admin(app):
    app.secret_key = os.environ.get('FLASK_APP_KEY', 'sample key')
    app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
    admin = Admin(app, name='4Geeks Admin', template_mode='bootstrap3')

    class FavoritesAdmin(ModelView):
        column_list = ("id","user_id", "characters_id", "planets_id", "vehicles_id")
        form_columns = ("characters_id", "planets_id", "vehicles_id")
        column_hide_backrefs = False

    
    # Add your models here, for example this is how we add a the User model to the admin
    admin.add_view(ModelView(User, db.session))
    admin.add_view(ModelView(Character, db.session))
    admin.add_view(ModelView(Planet, db.session))
    admin.add_view(ModelView(Vehicle, db.session))
    admin.add_view(FavoritesAdmin(Favorites, db.session))

    # You can duplicate that line to add mew models
    # admin.add_view(ModelView(YourModelName, db.session))