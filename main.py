import difflib
from sqlite3 import Date
from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from flask_datepicker import datepicker
from wtforms import StringField, SubmitField, TextAreaField, DateField
from wtforms.validators import DataRequired


app = Flask(__name__)
app.config['SECRET_KEY'] = "TailorApp Secret Key"
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///tailor.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

## INPUT FORM
class Measures(FlaskForm):
    name = StringField("Client Name", validators=[DataRequired()])
    shoulder = StringField("Shoulder")
    torso = StringField("Upper Body")
    arm = StringField("Arm Length")
    bicep = StringField("Arm Width")
    leg = StringField("Leg Length")
    lwidth = StringField("Leg Width")
    description = TextAreaField("Description")
    date = DateField('date')
    submit = SubmitField("Submit")


## CLIENT DATABASE
class Client(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    shoulder = db.Column(db.String(250))
    torso = db.Column(db.String(250))
    arm = db.Column(db.String(250))
    bicep = db.Column(db.String(250))
    leg = db.Column(db.String(250))
    lwidth = db.Column(db.String(250))
    description = db.Column(db.Text)

db.create_all()

@app.route("/", methods=['GET', 'POST'])
def home():
    clients = Client.query.all()
    clients = clients[::-1]
    return render_template("index.html", clients=clients)


@app.route("/add", methods=['GET', 'POST'])
def add():
    form = Measures()
    heyy = ['name', 'shoulder', 'torso', 'arm', 'bicep', 'leg', 'lwidth', 'description', 'date']
    if request.method == "POST":
        data = dict(request.form)
        print(data['date'])
        client = Client(
            name = data['name'], 
            shoulder = data['shoulder'],
            torso = data['arm'],
            bicep = data['bicep'],
            leg = data['leg'],
            lwidth = data['lwidth'],
            description = data['description'])
        # db.session.add(client)
        # db.session.commit()
        return redirect(url_for("home"))
    return render_template("add.html", form=form, heyy=heyy)


@app.route("/client/<int:client_id>")
def client_data(client_id):
    data = Client.query.get(client_id)
    return render_template("client.html", client=data)


@app.route("/results", methods=['GET', 'POST'])
def search():
    names = []
    clients = Client.query.all()
    data = dict(request.form)
    name = data['client']
    print(name)
    for client in clients:
        names.append(client.name)
    vals = difflib.get_close_matches(name, names)
    print(vals)
    clients = []
    for val in vals:
        cl = Client.query.filter_by(name = val).first()
        print(cl)
        clients.append(cl)
    print(clients)
    return render_template("search.html", clients=clients)


@app.route("/edit/<int:id>", methods=['GET', 'POST'])
def edit(id):
    heyy = ['name', 'shoulder', 'torso', 'arm', 'bicep', 'leg', 'lwidth', 'description', 'date']
    client = Client.query.get(id)
    form = Measures(
        name = client.name,
        shoulder = client.shoulder,
        torso = client.torso,
        arm = client.arm,
        bicep = client.bicep,
        leg = client.leg,
        lwidth = client.lwidth,
        description = client.description
    )
    if request.method == "POST":
        form = dict(request.form)
        client.name = form['name']
        client.shoulder = form['shoulder']
        client.torso = form['torso']
        client.arm = form['arm']
        client.bicep = form['bicep']
        client.leg = form['leg']
        client.lwidth = form['lwidth']
        client.description = form['description']
        db.session.commit()   
        return redirect(url_for("home"))

    return render_template("add.html", form=form, heyy=heyy)


@app.route('/delete/<int:xid>')
def delete(xid):
    client = Client.query.get(xid)
    db.session.delete(client)
    db.session.commit()
    return redirect(url_for('home'))



if __name__ == "__main__":
    app.run(debug=True)