from flask import Flask, render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todo.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class ToDo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(500), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.sno} - {self.title}"

# This will create the tables in the database
with app.app_context():
    db.create_all()  # Creates the tables

@app.route("/", methods=['GET', 'POST'])
def hello_world():
    if request.method=='POST':
        title = request.form ['title']
        desc = request.form['desc']
  
        # If no existing "first Todo", create one
        todo = ToDo(title=title, desc=desc)
        db.session.add(todo)
        db.session.commit()
    
    # Fetch all ToDo items from the database to display
    allToDo = ToDo.query.all()
    # Pass the list of todos to the template
    return render_template('index.html', allToDo = allToDo)

@app.route('/delete/<int:sno>')
def delete(sno):
    todo = ToDo.query.filter_by(sno=sno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect("/")

@app.route('/Update/<int:sno>', methods=['GET', 'POST'])
def update(sno):
    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['desc']
        todo = ToDo.query.filter_by(sno=sno).first()
       # Update the fields
        todo.title = title
        todo.desc = desc  
        db.session.commit()
        return redirect("/")
    todo = ToDo.query.filter_by(sno=sno).first()  
    return render_template('update.html', ToDo=todo)

if __name__ == "__main__":
    app.run(debug=True, port=8000)

