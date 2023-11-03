from flask import Flask, render_template, redirect, url_for, request, flash, g
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, TimeField
from wtforms.validators import InputRequired, Length, Email, ValidationError, Email, DataRequired
from wtforms.fields import DateField
from flask_bcrypt import Bcrypt
from datetime import datetime, date
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'  # Database URI
app.config["SECRET_KEY"] = "thisismysecret"  # Secret key for cookies
db = SQLAlchemy(app)  # Create the database
bcrypt = Bcrypt(app)


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)


class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=20)],
                           render_kw={'placeholder': 'Username'})
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=20)],
                             render_kw={'placeholder': 'Password'})
    first_name = StringField('First Name', validators=[InputRequired(), Length(max=50)],
                            render_kw={'placeholder': 'First Name'})
    last_name = StringField('Last Name', validators=[InputRequired(), Length(max=50)],
                           render_kw={'placeholder': 'Last Name'})
    email = StringField('Email', validators=[InputRequired(), Length(max=120), Email()],
                        render_kw={'placeholder': 'Email'})

    submit = SubmitField('Register')

    def validate_username(self, username):
        existing_user_username = User.query.filter_by(username=username.data).first()
        if existing_user_username:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        existing_user_email = User.query.filter_by(email=email.data).first()
        if existing_user_email:
            raise ValidationError('An account with this email already exists.')


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=20)],
                           render_kw={'placeholder': 'Username'})
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=20)],
                             render_kw={'placeholder': 'Password'})
    submit = SubmitField('Login')

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task_name = db.Column(db.String(255), nullable=False)
    tag = db.Column(db.String(255))
    priority = db.Column(db.String(255))
    date_start = db.Column(db.Date, nullable=False)
    date_end = db.Column(db.Date, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

class TaskForm(FlaskForm):
    task_name = StringField('Task Name', validators=[InputRequired(), Length(max=255)], render_kw={'placeholder': 'Enter task name'})
    tag = StringField('Tag', render_kw={'placeholder': 'Enter a tag'})
    priority = SelectField('Priority', choices=[('Not Important', 'Not Important'), ('Important', 'Important'), ('Extremely Important', 'Extremely Important')], render_kw={'placeholder': 'Select task priority'})
    date_start = DateField('Date Start', format='%Y-%m-%d', validators=[DataRequired()], render_kw={'placeholder': 'Select start date'})
    date_end = DateField('Date End', format='%Y-%m-%d', validators=[DataRequired()], render_kw={'placeholder': 'Select end date'})
    submit = SubmitField('Add Task')


class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    event_name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(255))
    event_date = db.Column(db.Date, nullable=False)
    event_time = db.Column(db.Time, nullable=False)
    link = db.Column(db.String(255))

    # Add a user_id column to link events to specific users
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Event('{self.event_name}', '{self.event_date}', '{self.event_time}')"

class EventForm(FlaskForm):
    event_name = StringField('Event Name', validators=[InputRequired(), Length(max=255)])
    description = StringField('Description', validators=[Length(max=255)])
    event_date = DateField('Event Date', format='%Y-%m-%d', validators=[InputRequired()])
    event_time = TimeField('Event Time')
    link = StringField('Link', validators=[Length(max=255)])

# Homepage
@app.route('/')
def home():
    return render_template('home.html')


# Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect(url_for('dashboard'))
            else:
                return redirect(url_for('login'))
    return render_template('login.html', form=form)


# Dashboard route (Displays tasks)
@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    tasks = Task.query.filter_by(user_id=current_user.id).order_by(Task.date_end.asc()).limit(3).all()
    events = Event.query.filter_by(user_id=current_user.id).order_by(Event.event_date.asc(), Event.event_time.asc()).limit(3).all()

    return render_template('dashboard.html', first_name=current_user.first_name, tasks=tasks, events=events)


# Logout
@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


# Register
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        new_user = User(
            username=form.username.data,
            password=hashed_password,
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            email=form.email.data
        )
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('login'))

    return render_template('register.html', form=form)




@app.route('/calendar')
def calendar():
    current_date = date.today()
    
    # Fetch the tasks for the current user
    tasks = Task.query.filter_by(user_id=current_user.id).all()
    
    return render_template('calendar.html', tasks=tasks, current_date=current_date)

# Task Management page (for adding and deleting tasks)
@app.route('/tasks/add', methods=['GET', 'POST'])
@login_required
def add_tasks():
    if request.method == 'POST':
        description = request.form.get('description')
        tag = request.form.get('tag')
        priority = request.form.get('priority')
        date_start_str = request.form.get('date_start')
        date_end_str = request.form.get('date_end')
        
        if description:
            date_start = datetime.strptime(date_start_str, '%Y-%m-%d').date()
            date_end = datetime.strptime(date_end_str, '%Y-%m-%d').date()

            new_task = Task(
                task_name = description,
                tag=tag,
                priority=priority,
                date_start=date_start,
                date_end=date_end,
                user_id=current_user.id
            )
            db.session.add(new_task)
            db.session.commit()
    
    tasks = Task.query.filter_by(user_id=current_user.id).all()
    return render_template('add_task.html', tasks=tasks)

# Function to fetch user's tags
def get_user_tags(user_id):
    if hasattr(g, 'db'):
        # Assuming you have a database connection stored in the 'g' object
        cursor = g.db.cursor()
        # Modify this SQL query to match your database schema
        cursor.execute("SELECT tag_name FROM user_tags WHERE user_id = %s", (user_id,))
        tags = [row[0] for row in cursor.fetchall()]
        return tags

    # If you're not using the 'g' object, you can fetch tags directly from your database here

    return []

# Add a new task (Task Management)
@app.route('/tasks', methods=['GET'])
@login_required
def tasks():
    now = datetime.now().date()
    tasks = Task.query.filter_by(user_id=current_user.id).all()
    task_dict = {}
    for task in tasks:
        tag = task.tag
        if tag not in task_dict:
            task_dict[tag] = []
        task_dict[tag].append(task)

    # Fetch the user's tags
    user_tags = get_user_tags(current_user.id)  # Implement this function to fetch the user's tags

    return render_template('tasks.html', tasks=tasks, now=now, task_dict=task_dict, user_tags=user_tags)

# Delete a task (Task Management)
@app.route('/tasks/delete/<int:task_id>', methods=['GET', 'POST'])
@login_required
def delete_task(task_id):
    task = Task.query.get(task_id)
    if task and task.user_id == current_user.id:
        db.session.delete(task)
        db.session.commit()
        return redirect(url_for('tasks'))  # Redirect back to the tasks page after deletion

    # Handle errors or unauthorized access as needed
    flash("Task not found or unauthorized.")
    return redirect(url_for('tasks'))

# Add an event creation route
@app.route('/events/create', methods=['GET', 'POST'])
@login_required
def create_event():
    if request.method == 'POST':
        event_name = request.form.get('event_name')
        description = request.form.get('description')
        link = request.form.get('link')
        event_date_str = request.form.get('event_date')
        event_time_str = request.form.get('event_time')

        if event_name:
            event_date = datetime.strptime(event_date_str, '%Y-%m-%d').date()
            event_time = datetime.strptime(event_time_str, '%H:%M').time()

            new_event = Event(
                event_name=event_name,
                description=description,
                link=link,
                event_date=event_date,
                event_time=event_time,
                user_id=current_user.id
            )
            db.session.add(new_event)
            db.session.commit()

    events = Event.query.filter_by(user_id=current_user.id).order_by(Event.event_date.asc(), Event.event_time.asc()).all()
    return render_template('create_events.html', events=events)


@app.route('/events')
def events():
    events = Event.query.filter_by(user_id=current_user.id).order_by(Event.event_date.asc(), Event.event_time.asc()).all()
    return render_template('events.html', events=events)

# Delete a event (Task Management)
@app.route('/events/delete/<int:event_id>', methods=['GET', 'POST'])
@login_required
def delete_event(event_id):
    event = Event.query.get(event_id)
    if event and event.user_id == current_user.id:
        db.session.delete(event)
        db.session.commit()
        return redirect(url_for('events'))  # Redirect back to the events page after deletion

    # Handle errors or unauthorized access as needed
    flash("Task not found or unauthorized.")
    return redirect(url_for('events'))


@app.route('/timer')
def timer():
    # Implement the timers page logic
    return render_template('timer.html')

if __name__ == '__main__':
    app.run(debug=True)
