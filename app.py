from flask import Flask
from backend.routes.vqe import vqe_bp
from backend.routes.qfold import qfold_bp
app = Flask(__name__)

# Register Blueprint
app.register_blueprint(vqe_bp, url_prefix="/vqe")
app.register_blueprint(qfold_bp, url_prefix="/qfold")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050, debug=True)