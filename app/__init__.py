from flask import Flask, app
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate

migrate = Migrate()

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    db.init_app(app)
    login_manager.init_app(app)

    login_manager.login_view = 'auth.login'
    migrate.init_app(app, db)

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

    app.register_blueprint(profile_bp)
    app.register_blueprint(transactions)
    app.register_blueprint(cards)
    app.register_blueprint(goals)
    app.register_blueprint(auth)
    app.register_blueprint(dashboard)
    app.register_blueprint(investments)

    return app