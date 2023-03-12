from flask import Flask
from countriesapi import countriesapi
from citiesapi import citiesapi
from temperaturesapi import temperaturesapi
from mainmembers import db

app = Flask(__name__)
app.register_blueprint(countriesapi)
app.register_blueprint(citiesapi)
app.register_blueprint(temperaturesapi)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@db:3306/app_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

if __name__ == '__main__':
    app.run('0.0.0.0', port=8080, debug=True)
