from flask import Flask
from .config import Config
from .extensions import db, cors

def create_app(config_class=None):
    # static_folder points to built frontend in production
    app = Flask(__name__, static_folder='../frontend/dist', static_url_path='/')
    if config_class is None:
        app.config.from_object(Config)
    else:
        app.config.from_object(config_class)

    db.init_app(app)
    cors.init_app(app, resources={r"/api/*": {"origins": "*"}})

    # register blueprints
    from .api.routes import api_bp
    app.register_blueprint(api_bp, url_prefix='/api')

    # serve built frontend index
    @app.route('/')
    def index():
        return app.send_static_file('index.html')

    return app
