from flask_wtf import FlaskForm
from wtforms import EmailField, PasswordField, StringField,SelectField
from wtforms.validators import InputRequired, Email


class LoginForm(FlaskForm):
    name=StringField('Name')
    email = EmailField(
        "Email address", [InputRequired("Please enter your email"), Email()]
    )
    password = PasswordField("Password", [InputRequired("Please enter your password")])
    role = SelectField('Choose role',choices=[('Admin','Admin'),('Driver','Driver'),('Accountance','Accountance')])
    