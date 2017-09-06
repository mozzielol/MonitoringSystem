#from app import db

#set the user model based on MongoDB. If you want to enable login function, please uncomment the code below. (You have to set the mongodb in __init__.py in app directory.)
'''
class User(db.Document):
    username = db.StringField(unique=True)
    password = db.StringField()
    email_addr = db.StringField()
    
    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return unicode(self.id)  # python 2
        except NameError:
            return str(self.id)  # python 3
    
    def __repr__(self):
        return '<%r>'%(self.username)
    
    def __str__(self):
        return '%s'%(self.username)


class Sensor_Data(db.Document):
    light_value = db.StringField()
    temp_value_celsius = db.StringField()
    temp_value_fahrenheit = db.StringField()
    humidity_value = db.StringField()
    UpdateTime = db.StringField()

'''