from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class todo(db.Model):
    __tablename__ = 'todo'
    sno = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(150), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    status = db.Column(db.String(500), nullable=False)
    date_time = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"{self.task} {self.description} {self.status} {self.date_time}"

@app.route("/", methods=['GET', 'POST'])
def add_todo():
    if request.method == 'POST':
        task = request.form.get('task')
        description = request.form.get('description')
        status = "Pending"
        if task and description:
            new_entry = todo(task=task, description=description, status=status)
            db.session.add(new_entry)
            db.session.commit()
    showing = todo.query.all()
    return render_template("index.html", showing=showing)

@app.route("/show")
def displaying():
    showing = todo.query.all()
    print(showing)
    return "Data printed in console"

@app.route("/delete/<int:sno>")
def delete(sno):
    todo_to_delete = todo.query.get_or_404(sno)
    db.session.delete(todo_to_delete)
    db.session.commit()
    return redirect("/")

@app.route("/update/<int:sno>", methods=["GET", "POST"])
def update(sno):
    todo_item = todo.query.get_or_404(sno)
    if request.method == "POST":
        todo_item.task = request.form.get("task")
        todo_item.description = request.form.get("description")
        todo_item.status = request.form.get("status")
        db.session.commit()
        return redirect("/")
    return render_template("update.html", todo=todo_item)


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
