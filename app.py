from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

import os

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("SQLALCHEMY_DATABASE_URI", "sqlite:///database.db")
app.secret_key = os.environ.get("SQLALCHEMY_SECRET_KEY", "CrefiNostalgie2022")
db = SQLAlchemy()
db.init_app(app)

class Configuratie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    max_score = db.Column(db.Integer)

class Pijler(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    score = db.Column(db.Integer, nullable=False)
    required_score = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"<Pijler {self.id}> {self.name}: {self.score}"

admin = Admin(app, name='Crefi Nostalgie', template_mode='bootstrap3')
admin.add_view(ModelView(Pijler, db.session))
admin.add_view(ModelView(Configuratie, db.session))

def get_max_score():
    config = Configuratie.query.first()

    if not config:
        config = Configuratie(max_score=1000)
        db.session.add(config)
        db.session.commit()

    return config.max_score

@app.route("/")
def root():
    pijlers = Pijler.query.all()
    max_score = get_max_score()
    return render_template("index.html", pijlers=pijlers, max_score=max_score)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run("0.0.0.0", 3000, debug=True)
