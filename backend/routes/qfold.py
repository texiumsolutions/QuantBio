import os
import logging
import uuid
from flask import Blueprint, request, jsonify
from backend.services.qfold_service import run_qfold
from backend.utils.azure_upload import upload_task_outputs

qfold_bp = Blueprint("qfold", __name__)

UPLOAD_FOLDER = "/home/texsols/QuantBio/algorithms/qfold/uploads"
OUTPUT_FOLDER = "/home/texsols/QuantBio/outputs/qfold_output"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

@qfold_bp.route("/predict", methods=["POST"])
def predict():
    try:
        task_id = str(uuid.uuid4())

        sequence = request.form.get("protein_sequence")
        peptide_name = request.form.get("peptide_name")
        rotation_bits = request.form.get("rotation_bits", 2)
        initialization = request.form.get("initialization", "minifold")
        mode = request.form.get("mode", "simulation")

        if not sequence or not peptide_name:
            logging.error("Missing required fields: protein_sequence or peptide_name.")
            return jsonify({"error": "Missing required fields: protein_sequence or peptide_name."}), 400

        params = {
            "task_id": task_id,
            "sequence": sequence,
            "peptide_name": peptide_name,
            "rotation_bits": rotation_bits,
            "initialization": initialization,
            "mode": mode
        }

        logging.info(f"Running QFold with task ID: {task_id} for sequence: {sequence}")
        result = run_qfold(params)
        return jsonify(result)

    except Exception as e:
        logging.error(f"Error in predict: {e}", exc_info=True)
        return jsonify({"error": str(e)}), 500


@qfold_bp.route("/check_status/<task_id>", methods=["GET"])
def check_status(task_id):
    try:
        task_folder = os.path.join(OUTPUT_FOLDER, task_id)
        log_file = os.path.join(task_folder, f"{task_id}.log")

        if not os.path.exists(log_file):
            logging.warning(f"Task ID {task_id} not found.")
            return jsonify({"error": "Task ID not found"}), 404

        with open(log_file, "r") as f:
            logs = f.readlines()

        azure_result = upload_task_outputs(task_id, task_folder)

        return jsonify({
            "task_id": task_id,
            "logs": logs,
            "azure_files": azure_result.get("uploaded_files", [])
        })

    except Exception as e:
        logging.error(f"Error in check_status: {e}", exc_info=True)
        return jsonify({"error": str(e)}), 500
