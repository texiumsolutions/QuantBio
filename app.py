from flask import Flask
from backend.routes.vqe import vqe_bp

app = Flask(__name__)

# Register Blueprint
app.register_blueprint(vqe_bp, url_prefix="/vqe")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050, debug=True)

