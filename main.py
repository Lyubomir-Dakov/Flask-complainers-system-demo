from decouple import config
from flask import Flask
from flask_migrate import Migrate
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://" \
                                        f"{config('DB_USER')}:" \
                                        f"{config('DB_PASSWORD')}" \
                                        f"@localhost:{config('DB_PORT')}" \
                                        f"/{config('DB_NAME')}"
db = SQLAlchemy(app)

migrate = Migrate(app, db)


if __name__ == "__main__":
    app.run(debug=True)
