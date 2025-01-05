from flask import render_template, request, flash, redirect, url_for
from app import create_app, db
from app.forms.loginform import LoginForm
from app.forms.routeform import RouteForm
from app.forms.shiftform import ShiftForm
from app.models import User, Routes, Stop, Shift
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import check_password_hash

app = create_app()


@app.route("/index")
@app.route("/")
def index():
    return render_template("index.html")


@app.route("/main")
def main():
    return render_template("main.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = request.form.get("email")
        password = request.form.get("password")
        remember_me = request.form.get("remember_me")
        user = User.query.filter_by(email=username).first()
        if not user or not check_password_hash(user.password_hash, password):
            flash("Please check your login details")
            return redirect(url_for("login"))
        login_user(user, remember=remember_me)
        return redirect(url_for("main"))
    return render_template("login.html", form=form)


@login_required
@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("index"))


@app.route("/create_route", methods=["GET", "POST"])
def create_route():
    form = RouteForm()
    if request.method == "POST":
        start_point = form.start_point.data
        end_point = form.end_point.data
        stops = form.stops.entries
        route = Routes(start_point=start_point, end_point=end_point)
        db.session.add(route)
        db.session.commit()
        for stop_form in stops:
            stop = Stop(location=stop_form.location.data, route_id=route.id)
            db.session.add(stop)
        db.session.commit()

        flash("Route created successfully!", "success")
        return redirect(url_for("create_route"))

    return render_template("create_route.html", form=form)


@app.route("/routes_list")
def routes_list():
    routes = Routes.query.all()
    return render_template("route_list.html", routes=routes)


@app.route("/delete_route/<int:id>", methods=["GET", "POST"])
def delete_route(id):
    route = Routes.query.filter_by(id=id).first()
    if route:
        for stop in route.stops:
            db.session.delete(stop)
        db.session.delete(route)
        db.session.commit()
    return redirect(url_for("routes_list"))


@app.route("/create_shift", methods=["GET", "POST"])
def create_shift():
    form = ShiftForm()
    if request.method == "POST":
        driver_id = form.driver.data
        route_id = form.route.data
        start_time = form.start_time.data
        end_time = form.end_time.data

        shift = Shift(
            driver_id=driver_id,
            route_id=route_id,
            start_time=start_time,
            approx_end_time=end_time,
        )
        db.session.add(shift)
        db.session.commit()
        flash("Shift created successfully")
        return redirect(url_for("shift_list"))

    return render_template("create_shift.html", form=form)


@app.route("/shift_list")
def shift_list():
    shifts = Shift.query.all()
    return render_template("shift_list.html", shifts=shifts)


@app.route("/delete_shift/<int:id>", methods=["GET", "POST"])
def delete_shift(id):
    shift = Shift.query.filter_by(id=id).first()
    db.session.delete(shift)
    db.session.commit()
    return redirect(url_for("shift_list"))


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
