from flask import Flask
from flask_mongoengine import MongoEngine
app = Flask(__name__)
app.config['MONGODB_SETTINGS'] = {
    'db': 'patent',
    'host': 'localhost',
    'port': 27017
}
db = MongoEngine(app)
class Equipment(db.Document):
    """
    This base class for all AI products
    """
    meta = {'allow_inheritance': True}
    sn = mongodb.StringField(unique=True)
    eq_name = mongodb.StringField()

All_data = Equipment.objects().all()