import os
from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from server.models import db

migrate = Migrate()

# Create and configure the app
def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    # Configure CORS
    CORS(app, resources={r"/*": {"origins": "*"}})
    db.init_app(app)
    migrate.init_app(app, db)

    from server.routes import bp
    app.register_blueprint(bp)

    with app.app_context():
        db.create_all()

    return app

app = create_app()

if __name__ == "__main__":
    app.run(port=5000, debug=True)


