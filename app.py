from flask import Flask


app = Flask(__name__,
            static_url_path='',
            template_folder="web/templates",
            static_folder='web/static',)
app.config.from_object('settings.Config')


from web.routes import *


if __name__ == '__main__':
    app.run(host='0.0.0.0')
