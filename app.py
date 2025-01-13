from flask import render_template, request, flash, redirect, url_for
from app import create_app, db
from app.forms.loginform import LoginForm
from app.forms.routeform import RouteForm
from app.forms.shiftform import ShiftForm
from app.forms.editshiftform import EditShiftForm
from app.forms.editrouteform import EditRouteForm
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

@app.route('/edit_route/<int:id>', methods=['GET', 'POST'])
def edit_route(id):
    form = EditRouteForm()
    route = Routes.query.get(id)
    form.start_point.data = route.start_point
    form.end_point.data = route.end_point

    # Pre-populate stops from the route
    for stop in route.stops:
        form.stops.append_entry({'location': stop.location})

    print(form.stops)
    if request.method == 'POST':
        route.start_point = form.start_point.data
        route.end_point = form.end_point.data

        # Get stops data from the form
        stops_data = request.form.getlist('stops[]')
        print("Submitted Stops Data:", stops_data)

        # Existing stops locations
        existing_stops = {stop.location: stop for stop in route.stops}  # Map locations to stop objects
        print("Existing Stops:", existing_stops)

        # Remove stops that are not in the updated list
        stops_to_remove = []
        for location, stop in existing_stops.items():
            if location not in stops_data:  # If the stop is no longer in the updated list, mark for deletion
                stops_to_remove.append(stop)

        for stop in stops_to_remove:
            db.session.delete(stop)

        # Add new stops (only those that are not already in the existing stops)
        for location in stops_data:
            if location not in existing_stops:  # If it's not an existing stop
                new_stop = Stop(location=location, route_id=route.id)
                db.session.add(new_stop)

        # Commit the changes to the database
        db.session.commit()
        flash("Route Edited successfully")
        return redirect(url_for('routes_list'))

    return render_template('edit_route.html', form=form, route=route)



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


@app.route("/edit_shift/<int:id>", methods=["GET", "POST"])
def edit_shift(id):
    form = EditShiftForm()
    shift = Shift.query.get(id)

    form.driver.data = shift.driver_id
    form.route.data = shift.route_id
    form.start_time.data = shift.start_time
    form.end_time.data = shift.approx_end_time

    if request.method == "POST":
        # Update the shift with the new form data
        shift.driver_id = form.driver.data
        shift.route_id = form.route.data
        shift.start_time = form.start_time.data
        shift.approx_end_time = form.end_time.data

        db.session.commit()  # Commit the changes to the database
        flash("Shift updated successfully", "success")
        return redirect(url_for("shift_list"))  # Redirect to the shift list page

    return render_template("edit_shift.html", form=form, shift=shift)


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
