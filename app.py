from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Photo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(150), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    status = db.Column(db.String(500), nullable=False)
    date_time = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"{self.task} {self.description} {self.status} {self.date_login}"
    
@app.route("/", methods=['GET', 'POST'])
def add_todo():
    if request.method == 'POST':
        task = request.form.get('task')
        description = request.form.get('description')
        status = "Pending"
        if task and description:
            new_entry = Photo(task=task, description=description,status=status)
            db.session.add(new_entry)
            db.session.commit()
    showing = Photo.query.all()
    return render_template("index.html", showing=showing)