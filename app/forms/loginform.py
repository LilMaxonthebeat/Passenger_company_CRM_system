from flask_wtf import FlaskForm
from wtforms import EmailField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email


class LoginForm(FlaskForm):
    email = EmailField(
        "Email address", [InputRequired("Please enter your email"), Email()]
    )
    password = PasswordField("Password", [InputRequired("Please enter your password")])
    remember_me = BooleanField("Remember me")
