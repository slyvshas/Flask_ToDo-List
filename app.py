from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime  

app = Flask(__name__, static_folder="static", template_folder="templates")

# Database Configuration
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///todo.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initialize Database
db = SQLAlchemy(app)

# Define the Todo Model
class Todo(db.Model):  
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(500), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.sno} - {self.title}"

# Routes
@app.route("/")
def homepage():
    all_todos = Todo.query.all()  # Fetch all todos
    return render_template("index.html", allTodos=all_todos)  

@app.route("/add_todo", methods=["POST"])
def add_todo():
    title = request.form["title"]
    desc = request.form["desc"]
    todo = Todo(title=title, desc=desc)
    db.session.add(todo)
    db.session.commit()
    return redirect(url_for("homepage"))

@app.route("/delete/<int:sno>")
def delete_todo(sno):
    todo = Todo.query.get_or_404(sno)
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for("homepage"))

# Run the app
if __name__ == "__main__":
    with app.app_context():
        db.create_all()  
    app.run(debug=True, port=8000)
