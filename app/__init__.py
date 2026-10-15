import os
from flask import Flask

from config import DATABASE_PATH
from app.database import close_db, init_db


BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)


def create_app(test_config=None):
    app = Flask(
        __name__,
        template_folder=os.path.join(BASE_DIR, "templates"),
    )

    app.config["DATABASE_PATH"] = DATABASE_PATH
    app.config["TESTING"] = False
    app.config["SECRET_KEY"] = "dev-key-change-later"

    if test_config:
        app.config.update(test_config)

    app.teardown_appcontext(close_db)

    from app.routes import main
    app.register_blueprint(main)

    with app.app_context():
        init_db()

    return app