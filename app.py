from flask import Flask,render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todo.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Todo(db.Model):
    sno= db.Column(db.Integer,primary_key=True)
    title= db.Column(db.String(200),nullable=False)
    desc=db.Column(db.String(400),nullable=False)
    date_created=db.Column(db.DateTime,default=datetime.utcnow)
   # Coloumns to be prinited when ToDo model object printed repr method call internally on print
    def __repr__(self):
        return f"{self.title}- {self.desc}"



@app.route("/",methods=['GET','POST'])
def home():
    alltodo = Todo.query.all()
    return render_template("index.html",alltodo=alltodo)

@app.route("/add",methods=['GET','POST'])
def add():
    if request.method=='POST':
        print(request.form['title'])
        todo = Todo(title=request.form['title'],desc=request.form['desc'])
        db.session.add(todo)
        db.session.commit()
    return redirect('/')

@app.route("/delete/<int:sno>")
def delete(sno):
    todelete = Todo.query.filter_by(sno=sno).first()
    print('todelete..............',todelete)
    db.session.delete(todelete)
    db.session.commit()
    return redirect('/')


@app.route("/update/<int:sno>", methods=['GET','POST'])
def update(sno):
    if request.method=='POST':
        title=request.form['title']
        desc=request.form['desc']
        todo = Todo.query.filter_by(sno=sno).first()
        todo.title=title
        todo.desc=desc
        db.session.add(todo)
        db.session.commit()
        return redirect('/')
    toupdate = Todo.query.filter_by(sno=sno).first()
    print('to_update,,,,',toupdate)
    return render_template('update.html',todo=toupdate)


if __name__ == "__main__":
    app.run(debug=True,port=8000)