from flask_wtf import FlaskForm
from wtforms import StringField, FieldList,SubmitField,FormField
from wtforms.validators import DataRequired


class StopForm(FlaskForm):
    location = StringField("Location", validators=[DataRequired()])


class RouteForm(FlaskForm):
    start_point = StringField("Start Point", validators=[DataRequired()])
    end_point = StringField("End Point", validators=[DataRequired()])
    stops = FieldList(FormField(StopForm), min_entries=1)
    submit = SubmitField("Create Route")
