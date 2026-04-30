import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate

migrate = Migrate()
db = SQLAlchemy()
login_manager = LoginManager()


def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    # Configuração do banco de dados
    database_url = os.getenv('DATABASE_URL')

    if database_url:
        if database_url.startswith('postgres://'):
            database_url = database_url.replace(
                'postgres://',
                'postgresql://',
                1
            )
        app.config['SQLALCHEMY_DATABASE_URI'] = database_url

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)

    login_manager.login_view = 'auth.login'

    from app.models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from .routes.auth import auth
    from .routes.dashboard import dashboard
    from .routes.investments import investments
    from .routes.goals import goals
    from .routes.cards import cards
    from .routes.transactions import transactions
    from .routes.profile import profile_bp
    from .routes.calculator import calculator_bp

    app.register_blueprint(auth)
    app.register_blueprint(dashboard)
    app.register_blueprint(investments)
    app.register_blueprint(goals)
    app.register_blueprint(cards)
    app.register_blueprint(transactions)
    app.register_blueprint(profile_bp)
    app.register_blueprint(calculator_bp)

    with app.app_context():
        db.create_all()

    return app