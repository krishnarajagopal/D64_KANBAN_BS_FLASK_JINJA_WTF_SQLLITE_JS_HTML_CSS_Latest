import json
from flask import Flask, render_template, request, redirect, url_for, flash,jsonify
from flask_bootstrap import Bootstrap5
from faker import Faker
from faker.providers import DynamicProvider,BaseProvider
from flask_wtf import FlaskForm
from wtforms import DecimalField,FloatField
from wtforms.fields import TimeField, URLField, StringField, SubmitField,SelectField,DateField,IntegerRangeField,IntegerField,TextAreaField,DateField
from wtforms.validators import DataRequired, URL, NoneOf, NumberRange,Regexp
from wtforms_validators import AlphaSpace
import sqlite3
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect

# from flask_modals import render_template_modal
# from flask_modals import Modal

# '''
# Red underlines? Install the required packages first: 
# Open the Terminal in PyCharm (bottom left). 

# On Windows type:
# python -m pip install -r requirements.txt

# On MacOS type:
# pip3 install -r requirements.txt

# This will install the packages from requirements.txt for this project.
# '''
db = SQLAlchemy()
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///new_defects_collection.db"
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
csrf = CSRFProtect(app)
db.init_app(app)
bootstrap = Bootstrap5(app)

class Task(db.Model):
    __tablename__ = 'tasks'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    description = db.Column(db.String(250), unique=False, nullable=False)
    name_assignee = db.Column(db.String(50), unique=False, nullable=False)
    status = db.Column(db.String(50), unique=False, nullable=False)
    due_date=db.Column(db.Date, unique=False, nullable=False)
    percent_complete = db.Column(db.Integer, nullable=False)

faker_status=DynamicProvider(
    provider_name="task_status",
    elements=["TO DO", "IN PROGRESS", "REVIEW", "COMPLETE"],
)

fake=Faker(locale='en_US')
fake.add_provider(faker_status)
Faker.seed(0)

# ##Use this to create a DICTIONARY of Dictionaries of Fake data
# tasks = {}
# for i in range(0, 3):
#     tasks[i]={}
#     tasks[i]['id'] = i+1
#     tasks[i]['title'] = fake.sentence(nb_words=3)
#     tasks[i]['description'] = fake.paragraph(nb_sentences=1)
#     tasks[i]['name_assignee'] = fake.name()
#     tasks[i]['status'] = fake.task_status()
#     tasks[i]['due_date'] = fake.date_this_month(before_today=False, after_today=True)
#     tasks[i]['percent_complete'] = fake.random_int(min= 0, max= 100, step= 1)
# print(tasks)

##Use this to create a LIST of Dictionaries of Fake data
task = {}
tasks=[]
for i in range(0, 30):
    task['id'] = i+1
    task['title'] = fake.sentence(nb_words=3)
    task['description'] = fake.paragraph(nb_sentences=5)
    task['name_assignee'] = fake.name()
    task['status'] = fake.task_status()
    task['due_date'] = fake.date_this_month(before_today=False, after_today=True)
    task['percent_complete'] = fake.random_int(min= 0, max= 100, step= 1)
    tasks.append(task.copy())
#     print(task)
# print(tasks)

##Create Table
with app.app_context():
    db.create_all()


#Insert Initial Fake Rows:

with app.app_context():
    record_exists = db.session.query(db.session.query(Task).filter_by(id=1).exists()).scalar()
    if not record_exists:
        for task_item in tasks:
            add_new_task_to_db = Task(**task_item)
            db.session.add(add_new_task_to_db)
            db.session.commit()


class update_task_form(FlaskForm):
    id = IntegerField(label='Task ID', validators=[DataRequired()], render_kw={'readonly': True})
    title = StringField(label='Title')
    description = TextAreaField (label='Description',  validators=[DataRequired()])
    name_assignee=StringField (label='Name Assignee', validators=[DataRequired(),AlphaSpace()])
    status=SelectField (label='Status', choices=["TO DO", "IN PROGRESS", "REVIEW", "COMPLETE"],coerce=str,validate_choice=True,validators=[DataRequired()])
    due_date=DateField (label='Due Date', validators=[DataRequired(message="Valid due Date required")])
    percent_complete = IntegerField (label="Percent Complete",validators=[DataRequired(),NumberRange(min=0,max=100,message="Enter a number between 0 and 100")])
    submit = SubmitField(label='Update Task')


def get_tasks():
    result = db.session.execute(db.select(Task).order_by(Task.due_date))
    all_db_tasks = result.scalars()
    return all_db_tasks

@app.route('/', methods=['GET','POST'])
def home():
    form=update_task_form()
    if request.method == 'GET':
        all_tasks=get_tasks() 
        #    print(all_tasks)
        return render_template('index.html',tasks=list(all_tasks),form=form)
    elif  request.method=='POST' and form.validate_on_submit():
        task_id=request.form.get('id')
        task_to_edit = db.get_or_404(Task, task_id)
        print(f'Task ID to DB: {task_id}')
        # print(f'Task ID from DB: {db_result_to_update}')
        # print(f"Title:{form.title.data}, Description:{form.description.data}, Name_Assignee:{form.name_assignee.data},Status:{form.status.data},due_date:{form.due_date.data},percent_complete:{form.percent_complete.data}")
        task_to_edit.title = form.title.data
        task_to_edit.description = form.description.data 
        task_to_edit.name_assignee = form.name_assignee.data
        task_to_edit.status = form.status.data
        task_to_edit.due_date = form.due_date.data
        task_to_edit.percent_complete = form.percent_complete.data
        db.session.commit()
        flash(f"Task Details for : { task_to_edit.title} updated successfully",category="alert-success")
        return redirect(url_for("home"))
    else:
       return redirect(url_for("home"))


@app.route('/postmethod', methods = ['POST'])
def post_status_update_data():
    jsdata = request.get_json(force=True,)
    print (f"\nID: {jsdata['id']},\nStatus: {jsdata['status']}")
    id = jsdata['id']
    task_to_edit = db.get_or_404(Task, id)
    task_to_edit.status = jsdata['status']
    db.session.commit()
    flash(f"Status for Task Title ' {task_to_edit.title} ': updated successfully to '{ task_to_edit.status}' ",category="alert-success")
    return jsonify({'status':'success'})
    
@app.route("/add", methods=[ "POST"])
def add():
    form=update_task_form()
    if request.method == "POST":
        # print(f"\
        # title = {form.title.data}\
        # description = {form.description.data} \
        # name_assignee = {form.name_assignee.data}\
        # status = {form.status.data}\
        # due_date = {form.due_date.data}\
        # percent_complete = {form.percent_complete.data}\
        # percent_complete = {request.form['percent_complete']}")
        new_task=Task(
        title = form.title.data,
        description = form.description.data, 
        name_assignee = form.name_assignee.data,
        status = form.status.data,
        due_date = form.due_date.data,
        percent_complete = form.percent_complete.data,)
        db.session.add(new_task)
        db.session.commit()
        flash(message=f"Book Name : {new_task.title} Added successfully", category="alert-success")
        return redirect(url_for('home'))

@app.route("/delete", methods=["POST"])
def delete():
    # if  request.method=='POST' :
    task_id=request.form.get('id')
    task_to_delete = db.get_or_404(Task, task_id)
    # print(f'Method: {request.method}\nTask ID to be deleted in DB: {task_id}\nTask retreived from DB: {task_to_delete.id}')
    db.session.delete(task_to_delete)
    db.session.commit()
    flash(message= f"Task Name : {task_to_delete.title} Deleted successfully",category="alert-danger")
    return redirect(url_for('home'))

if __name__ == "__main__":
    app.run(debug=True, port=5001)
