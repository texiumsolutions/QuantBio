import os
import logging
import uuid
import urllib.parse
import requests
from flask import Blueprint, request, jsonify
from backend.services.vqe_service import run_vqe
from backend.utils.azure_upload import upload_task_outputs

vqe_bp = Blueprint("vqe", __name__)

UPLOAD_FOLDER = "/home/texsols/QuantBio/algorithms/protein-folding/uploads"
OUTPUT_FOLDER = "/home/texsols/QuantBio/outputs/vqe_output"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def download_file(url, save_path):
    try:
        response = requests.get(url, stream=True, timeout=10)
        response.raise_for_status()
        with open(save_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
        logging.info(f"Downloaded file from URL to {save_path}")
        return save_path
    except requests.exceptions.RequestException as e:
        logging.error(f"Download failed from URL: {url} - {e}")
        raise Exception(f"Download failed from URL: {url} - {e}")

@vqe_bp.route("/predict", methods=["POST"])
def predict():
    try:
        task_id = str(uuid.uuid4())
        sequence = request.form.get("protein_sequence")

        if not sequence:
            logging.error("No protein sequence provided.")
            return jsonify({"error": "No protein sequence provided."}), 400

        params = {
            "task_id": task_id,
            "sequence": sequence
        }

        logging.info(f"Running VQE with task ID: {task_id} for sequence: {sequence}")
        result = run_vqe(params)
        return jsonify(result)

    except Exception as e:
        logging.error(f"Error in predict: {e}", exc_info=True)
        return jsonify({"error": str(e)}), 500


@vqe_bp.route("/check_status/<task_id>", methods=["GET"])
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
