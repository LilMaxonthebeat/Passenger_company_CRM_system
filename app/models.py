from app import db, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class User(UserMixin, db.Model):
    __tablename__ = "User"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, index=True, nullable=False)
    email = db.Column(db.String, index=True, nullable=False, unique=True)
    password_hash = db.Column(db.String, nullable=False)
    role = db.Column(db.Integer, index=True, nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


class Routes(db.Model):
    __tablename__ = "routes"
    id = db.Column(db.Integer, primary_key=True)
    start_point = db.Column(db.String, nullable=False)
    end_point = db.Column(db.String, nullable=False)
    stops = db.relationship("Stop", backref="route", lazy=True)


class Stop(db.Model):
    __tablename__ = "stops"
    id = db.Column(db.Integer, primary_key=True)
    location = db.Column(db.String())
    route_id = db.Column(db.Integer, db.ForeignKey("routes.id"), nullable=False)

class Busses(db.Model):
    __tablename__="busses"
    id=db.Column(db.Integer primary_key=True)
    name=db.Column(db.String())
    register_number=db.Column(db.String())
    inspection_valid=db.Column(db.DateTime,nullable=False)

class Shift(db.Model):
    __tablename__ = "shifts"
    id = db.Column(db.Integer, primary_key=True)
    driver_id = db.Column(db.Integer, db.ForeignKey("User.id"), nullable=False)
    route_id = db.Column(db.Integer, db.ForeignKey("routes.id"), nullable=False)
    driver = db.relationship(
        "User", backref="shifts", lazy=True
    )  # Link to the actual driver
    route = db.relationship(
        "Routes", backref="shifts", lazy=True
    )  # Link to the actual route
    # Start time and approximate end time for the shift
    start_time = db.Column(db.DateTime, nullable=False)
    approx_end_time = db.Column(db.DateTime, nullable=True)


