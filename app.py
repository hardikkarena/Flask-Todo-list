from email.policy import default
from msilib.schema import Class
from flask import Flask,render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import PrimaryKeyConstraint, false, true
from datetime import datetime

app = Flask(__name__)

# app.config['SQLALCHEMY_DATABSE_URI'] = "sqlite:///todo.db"
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
class Todo(db.Model):
    sno=db.Column(db.Integer,primary_key=true)
    title=db.Column(db.String(200),nullable=false)
    dec=db.Column(db.String(500),nullable=false)
    date_created=db.Column(db.DateTime(500),default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.sno} - {self.title}"  




@app.route('/')
def index():
    all_todo = Todo.query.all()
    print(type(all_todo))
 
    return render_template('index.html',todo=all_todo)


@app.route('/create',methods=['GET','POST'])
def create():
    if request.method == 'POST':
        title = request.form['title']
        dec = request.form['dec']
        new_todo = Todo(title=title,dec=dec)
        db.session.add(new_todo)
        db.session.commit()
        
    return redirect("/")

@app.route('/update/<int:sno>',methods=['GET','POST'])
def update(sno):
    if request.method == 'POST':
        title = request.form['title']
        dec = request.form['dec']
        todo = Todo.query.get(sno)
        todo.title = title
        todo.dec = dec
        db.session.commit()
        return redirect("/")
    else:
        todo = Todo.query.get(sno)
        return render_template('update.html',todo=todo)


        
    # return 'Hello, World! sbadjabsdnadsma'
@app.route('/delete/<int:sno>',)
def delete(sno):

    # del_todo = Todo.query.filter_by(sno=sno).first()
    del_todo = Todo.query.get(sno)
    db.session.delete(del_todo)
    db.session.commit()
    return redirect("/")
    # return 'Hello, World! sbadjabsdnadsma'

@app.route('/home')
def home():
    todo = Todo(title="Srock Market",dec="Start Investing In stock Market")
    db.session.add(todo) 
    db.session.commit()
    return 'This is Home'

if __name__ == "__main__":
    app.run(debug=True,port=7000),