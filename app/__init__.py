import os
from datetime import timedelta

from flask import Flask, render_template, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from werkzeug.exceptions import HTTPException

# instantiate extensions
login_manager = LoginManager()
db = SQLAlchemy()
migrate = Migrate()


def create_app(environment='development'):

    from config import config
    from app.views import (
        main_blueprint,
        auth_blueprint,
        account_blueprint,
        user_blueprint,
        reseller_blueprint,
        distributor_blueprint,
        sub_reseller_blueprint,
        product_blueprint,
    )
    from app.models import (
        User,
        AnonymousUser,
    )

    # Instantiate app.
    app = Flask(__name__)

    # Set app config.
    env = os.environ.get('FLASK_ENV', environment)
    app.config.from_object(config[env])
    app.config['JSON_SORT_KEYS'] = False
    config[env].configure(app)

    # Set up extensions.
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    # Register blueprints.
    app.register_blueprint(auth_blueprint)
    app.register_blueprint(main_blueprint)
    app.register_blueprint(account_blueprint)
    app.register_blueprint(user_blueprint)
    app.register_blueprint(reseller_blueprint)
    app.register_blueprint(distributor_blueprint)
    app.register_blueprint(sub_reseller_blueprint)
    app.register_blueprint(product_blueprint)

    # Set up flask login.
    @login_manager.user_loader
    def get_user(id):
        return User.query.get(int(id))

    login_manager.login_view = 'auth.login'
    login_manager.login_message_category = 'info'
    login_manager.anonymous_user = AnonymousUser

    # Error handlers.
    @app.errorhandler(HTTPException)
    def handle_http_error(exc):
        return render_template('error.html', error=exc), exc.code

    @app.before_request
    def before_request():
        session.permanent = True
        app.permanent_session_lifetime = timedelta(minutes=int(os.environ.get('SESSION_EXPIRY_TIME', 15)))

    return app
