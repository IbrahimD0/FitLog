from flask import Flask, render_template, url_for, redirect, flash, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, \
    logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask_bcrypt import Bcrypt
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import datetime

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SECRET_KEY'] = 'thisisasecretkey'

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)
    workouts = db.relationship('Workout', backref='user')
    daily_workouts = db.relationship('DailyWorkout', backref='user')


class Workout(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    exercises = db.relationship('Exercise', backref='workout', cascade='all, delete-orphan')


class Exercise(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    reps = db.Column(db.String(20), nullable=False)
    sets = db.Column(db.String(20), nullable=False)
    workout_id = db.Column(db.Integer, db.ForeignKey('workout.id'))


class DailyWorkout(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)
    duration = db.Column(db.Interval, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    daily_exercises = db.relationship('DailyExercise', backref='daily_workout', cascade='all, delete-orphan')


class DailyExercise(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    reps = db.Column(db.String(20), nullable=False)
    sets = db.Column(db.String(20), nullable=False)
    weights = db.Column(db.Float(20), nullable=False)
    daily_workout_id = db.Column(db.Integer, db.ForeignKey('daily_workout.id'))


with app.app_context():
    db.create_all()


@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()
        if user:
            if bcrypt.check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('homepage'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Username does not exist.', category='error')

    return render_template("login.html", user=current_user)


@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    if logout_user():
        flash('User Logged out successfully!', category='success')
    return redirect(url_for('login'))


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        print(request.form)
        username = request.form.get('username')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(username=username).first()
        if user:
            flash('Username already exists.', category='error')
        elif len(username) < 4:
            flash('Username must be greater than 3 characters.',
                  category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        else:
            hashed_password = bcrypt.generate_password_hash(password1).decode('utf-8')
            new_user = User(username=username, password=hashed_password)

            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)

            flash('Account created!', category='success')
            return redirect(url_for('login'))

    return render_template('signup.html')


@app.route('/homepage', methods=['GET', 'POST'])
def homepage():
    return render_template('homepage.html')


@app.route('/workout', methods=['GET', 'POST'])
@login_required
def work_out():
    if request.method == "POST":
        workoutName = request.form.get('workoutName')
        exerciseNames = request.form.getlist('name[]')
        reps = request.form.getlist('reps[]')
        sets = request.form.getlist('sets[]')

        workout = Workout(name=workoutName, user_id=current_user.id)
        db.session.add(workout)
        db.session.commit()

        for i in range(len(exerciseNames)):
            exercise = Exercise(name=exerciseNames[i], reps=reps[i],
                                sets=sets[i], workout_id=workout.id)
            db.session.add(exercise)
            db.session.commit()

        flash('Workouts saved successfully!', category='success')

    return render_template('workout.html', user=current_user)


@login_required
@app.route('/routines', methods=['GET', 'POST'])
def routines():
    return render_template('routines.html', user=current_user)


@login_required
@app.route("/delete_workout", methods=["POST"])
def delete_workout():
    workout_id = request.form.get("workout_id")
    # Perform the deletion of the workout from the database using the workout_id
    workout = Workout.query.get(workout_id)

    if workout:
        # Remove the workout from the database
        db.session.delete(workout)
        db.session.commit()

    # Redirect back to the routines page or any other desired page
    return redirect("/routines")


@login_required
@app.route("/startworkout", methods=["GET", "POST"])
def start_workout():
    workout_id = request.form.get("workout_id")
    # Fetch the workout from the database using the workout_id
    workout = Workout.query.get(workout_id)

    return render_template('startworkout.html', workout=workout)


@app.route('/progress', methods=['GET', 'POST'])
def display_workouts():



    return render_template('progress.html', user=current_user)


@app.route("/finish_workout", methods=["GET", "POST"])
def finish_workout():
    if request.method == "POST":
        print(request.form)

        date_today = datetime.date.today()
        workout_id = request.form.get('workout_id')
        workout = Workout.query.get(workout_id)

        format_duration = request.form.get('duration')
        try:
            hours, minutes, seconds = map(int, format_duration.split(':'))
        except ValueError:
            # Handle the case when one or more components are missing or not integers
            return "Invalid duration format", 400
        workout_duration = datetime.timedelta(hours=hours, minutes=minutes, seconds=seconds)

        daily_workout = DailyWorkout(name=workout.name, date=date_today, user=current_user, duration=workout_duration)
        db.session.add(daily_workout)
        db.session.commit()
        exercise_names = request.form.getlist('exercise_name[]')
        exercise_reps = request.form.getlist('exercise_rep[]')
        exercise_sets = request.form.getlist('exercise_set[]')
        exercise_weights = request.form.getlist('exercise_weight[]')

        for name, reps, sets, weight in zip(exercise_names, exercise_reps, exercise_sets, exercise_weights):
            daily_exercise = DailyExercise(
                name=name,
                reps=reps,
                sets=sets,
                weights=weight,
                daily_workout=daily_workout
            )
            db.session.add(daily_exercise)

        db.session.commit()

        return render_template('progress.html', user=current_user)

@app.route("/history", methods=["GET", "POST"])
def progress_history():
    return render_template('history.html', user=current_user)


if __name__ == "__main__":
    app.run(debug=True)
