import os
from flask import Flask
#from flask_login import LoginManager
#from flask_mongoengine import MongoEngine
'''
The code commented out is used to set the MongoDB and enable login function. You can create a account in 'https://mlab.com/login/'.
'''

app = Flask(__name__)
app.config.from_object('config')

'''
#This is used to set the configuration of your mongodb
app.config['MONGODB_SETTINGS'] = {
    'db': THE NAME OF YOUR DATABASE,
    'host': THE ADDRESS OF YOUR DATABASE,
    'username':YOUR MONGODB USER ACCOUNT,
    'password':YOUR MONGODB USER PASSWORD
}
db = MongoEngine()
db.init_app(app)
lm = LoginManager()
lm.init_app(app)
'''
app.secret_key = 'youdontknowme'



from app import views,models
