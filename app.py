from flask import Flask, render_template, url_for, redirect, flash, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, \
    logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SECRET_KEY'] = 'thisisasecretkey'

db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)
    workouts = db.relationship('Workout', backref='user')


class Workout(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    exercises = db.relationship('Exercise', backref='workout',
                                cascade='all, delete-orphan')


class Exercise(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    reps = db.Column(db.String(20), nullable=False)
    sets = db.Column(db.String(20), nullable=False)
    workout_id = db.Column(db.Integer, db.ForeignKey('workout.id'))


with app.app_context():
    db.create_all()


@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()
        if user:
            if check_password_hash(user.password, password):
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
    return redirect(url_for('login'))


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
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
            new_user = User(username=username, password=generate_password_hash(
                password1, method='sha256'))

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
        workoutNames = request.form.getlist('workoutName')
        exerciseNames = request.form.getlist('name[]')
        reps = request.form.getlist('reps[]')
        sets = request.form.getlist('sets[]')

        for i in range(len(workoutNames)):
            workout = Workout(name=workoutNames[i], user_id=current_user.id)
            db.session.add(workout)
            db.session.commit()

            for j in range(len(exerciseNames)):
                exercise = Exercise(name=exerciseNames[j], reps=reps[j],
                                    sets=sets[j], workout_id=workout.id)
                db.session.add(exercise)
                db.session.commit()

        flash('Workouts saved successfully!', category='success')

    return render_template('workout.html', user=current_user)


@app.route('/progress', methods=['GET', 'POST'])
def display_workouts():
    return render_template('progress.html', user=current_user)


@app.route('/routines', methods=['GET', 'POST'])
def routines():
    return render_template('routines.html', user=current_user)


if __name__ == "__main__":
    app.run(debug=True)
