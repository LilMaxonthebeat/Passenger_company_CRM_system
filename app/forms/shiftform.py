from flask_wtf import FlaskForm
from wtforms import (
    SubmitField,
    SelectField,
    DateTimeLocalField,
)
from wtforms.validators import DataRequired


from app.models import Routes, User


class ShiftForm(FlaskForm):
    driver = SelectField("Driver", coerce=int, validators=[DataRequired()])
    route = SelectField("Route", coerce=int, validators=[DataRequired()])
    start_time = DateTimeLocalField(
        "Start Time", format="%Y-%m-%dT%H:%M", validators=[DataRequired()]
    )
    end_time = DateTimeLocalField(
        "Approximate End Time", format="%Y-%m-%dT%H:%M", validators=[DataRequired()]
    )
    submit = SubmitField("Create Shift")

    def __init__(self, *args, **kwargs):
        super(ShiftForm, self).__init__(*args, **kwargs)

        # Populate the driver select field with all users with role=1 (assuming 1 is the role for drivers)
        self.driver.choices = [
            (user.id, user.name) for user in User.query.filter_by(role='Driver').all()
        ]

        # Populate the route select field with all routes
        self.route.choices = [
            (route.id, route.start_point + " to " + route.end_point)
            for route in Routes.query.all()
        ]
