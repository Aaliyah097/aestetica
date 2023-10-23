import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__,
            static_url_path='',
            template_folder="web/templates",
            static_folder='static',)
app.config.from_object('settings.Config')
app.config['FLASK_ADMIN_SWATCH'] = 'lux'


from db.aestetica.tables import Base


db = SQLAlchemy(model_class=Base)
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///' + os.path.abspath('db/aestetica/db.sqlite3')
db.init_app(app)


from admin import *


from web.routes import *


if __name__ == '__main__':
    app.run(host='0.0.0.0')
