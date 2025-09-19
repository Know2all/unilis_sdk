from socket_server import SocketServer
from flask import Flask
from extensions import db
from routes import bp as api_bp
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    CORS(app)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Initialize extensions
    db.init_app(app)

    # Register blueprints
    app.register_blueprint(api_bp, url_prefix="/api")

    # Create tables if not exist
    with app.app_context():
        db.create_all()

    return app

app = create_app()

if __name__ == "__main__":
    # Start socket server in background
    server = SocketServer(host="0.0.0.0", port=9001, callback_url="http://127.0.0.1:5000/api/data")
    server.start()
    # Start Flask app
    app.run(host="0.0.0.0", port=5000, debug=True)