from flask import Flask, jsonify
from flask_jwt_extended import JWTManager

from config import Config
from models import db, User  # noqa: F401
from routes import auth_bp

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
with app.app_context():
    db.create_all()

JWTManager(app)
app.register_blueprint(auth_bp)


@app.errorhandler(400)
def bad_request(error):
    return jsonify(message="Bad Request", error=str(error)), 400


@app.errorhandler(401)
def unauthorized(error):
    return jsonify(message="Unauthorized", error=str(error)), 401


@app.errorhandler(404)
def not_found(error):
    return jsonify(message="Not Found", error=str(error)), 404


@app.errorhandler(500)
def internal_error(error):
    return jsonify(message="Internal Server Error", error=str(error)), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8181, debug=True)
