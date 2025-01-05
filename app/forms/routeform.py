from flask_wtf import FlaskForm
from wtforms import StringField, FieldList,SubmitField,FormField
from wtforms.validators import DataRequired


class StopForm(FlaskForm):
    """Form for adding a stop to a route."""

    location = StringField("Location", validators=[DataRequired()])


class RouteForm(FlaskForm):
    start_point = StringField("Start Point", validators=[DataRequired()])
    end_point = StringField("End Point", validators=[DataRequired()])

    # Allows the user to add multiple stops
    stops = FieldList(FormField(StopForm), min_entries=1, label="Stops")

    submit = SubmitField("Create Route")
