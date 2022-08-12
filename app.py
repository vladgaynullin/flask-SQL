from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///clients.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Table(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    age = db.Column(db.Integer(), nullable=False)

    def __repr__(self):
        #return "<{}:{}:{}>".format(self.name, self.age)
        return '<Table %r>' % self.id

@app.route('/')
@app.route('/home')
def home():
    return render_template("home.html")


@app.route('/add', methods=['POST', 'GET'])
def add():
    if request.method == "POST":
        name = request.form['name']
        age = request.form['age']

        table = Table(name=name, age=age)

        try:
            db.session.add(table)
            db.session.commit()
            return redirect('/')
        except Exception as e:
            return "При добавлении произошла ошибка"

    else:
        return render_template("add.html")

@app.route('/users', methods=['GET', 'POST'])
def users():
    all_users = Table.query.all()
    return render_template("users.html", all_users=all_users)

@app.route('/user_<int:id>')
def user(id):
    user_x = Table.query.get(id)
    return render_template("user_x.html", user_x=user_x)

if __name__ == "__main__":
    app.run(debug=True)
