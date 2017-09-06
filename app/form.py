from flask_wtf import Form
from wtforms import StringField,PasswordField
from wtforms.validators import DataRequired

class LoginForm(Form):
    username = StringField('username',validators=[DataRequired()])
    password = PasswordField('password',validators=[DataRequired()])


class SettingForm(Form):
    username_setting = StringField('username_setting',validators=[DataRequired()])
    password_setting = PasswordField('password_setting',validators=[DataRequired()])
    password_setting_verify = PasswordField('password_setting_verify',validators=[DataRequired()])
    email_addr_setting = StringField('email_addr_setting')
    

class PswChangeForm(Form):
    password_new = PasswordField('password_new',validators=[DataRequired()])
    password_new_verify = PasswordField('password_new_verify',validators=[DataRequired()])

class EmailChangeForm(Form):
    email_addr_new = StringField('email_addr_new',validators=[DataRequired()])
    email_addr_new_verify = StringField('email_addr_new_verify',validators=[DataRequired()])
    
class LcdForm(Form):
    lcdmsg = StringField('email_addr_new',validators=[DataRequired()])

class FaceForm(Form):
    name = StringField('name',validators=[DataRequired()])