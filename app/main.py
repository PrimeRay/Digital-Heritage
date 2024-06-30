from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from app.config import Config

db = SQLAlchemy()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)

    from app.api.events import events_bp
    app.register_blueprint(events_bp)

    from app.api.health import health_bp
    app.register_blueprint(health_bp)

    @app.route('/')
    def index():
        return render_template('index.html')

    return app