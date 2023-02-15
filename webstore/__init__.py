from flask import Flask, render_template
from flask_bootstrap import Bootstrap4
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

app = Flask(__name__)


def create_app():
    app.debug = True
    app.secret_key='BetterSecretNeeded123'

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///growdb.sqlite'

    db.init_app(app)

    bootstrap = Bootstrap4(app)

    from . import views
    app.register_blueprint(views.bp)

    return app


@app.errorhandler(404)
# inbuilt function which takes error as parameter
def not_found(e):
  return render_template("404.html")

@app.errorhandler(500)
def internal_error(e):
  return render_template("500.html")
