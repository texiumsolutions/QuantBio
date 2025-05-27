import os
import subprocess
import logging
from backend.utils.azure_upload import upload_task_outputs

QFOLD_SCRIPT = os.path.abspath("/home/texsols/QuantBio/algorithms/QFold/main.py")
OUTPUT_FOLDER = os.path.abspath("/home/texsols/QuantBio/outputs/Qfold_output")
CONDA_ENV_NAME = "qfold38"  # same as VQE for now

os.makedirs(OUTPUT_FOLDER, exist_ok=True)
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def get_file_type(file_path):
    ext = os.path.splitext(file_path)[-1].lower()
    if ext == '.csv':
        return 'csv'
    elif ext == '.txt':
        return 'txt'
    elif ext == '.pdb':
        return 'pdb'
    elif ext == '.log':
        return 'log'
    else:
        return 'unknown'

def generate_azure_link(task_id, file_name):
    base_url = "https://biotex.blob.core.windows.net/proteinfold/outputs/qfold_output"
    sas_token = "?sp=r&st=2025-04-24T18:49:42Z&se=2025-12-06T03:49:42Z&spr=https&sv=2024-11-04&sr=c&sig=DKTFbrdckeXxXPqxb0Nc%2Fn9vEz6lwR%2FudFYcj9XmugQ%3D"
    return f"{base_url}/{task_id}/{file_name}{sas_token}"

def run_qfold(params):
    task_id = params["task_id"]
    peptide_name = params["peptide_name"]
    sequence = params["sequence"]
    rotation_bits = params.get("rotation_bits", 2)
    initialization = params.get("initialization", "minifold")
    mode = params.get("mode", "simulation")

    task_output_folder = os.path.join(OUTPUT_FOLDER, task_id)
    os.makedirs(task_output_folder, exist_ok=True)

    output_log = os.path.join(task_output_folder, f"{task_id}.log")

    command = f"""
    source ~/miniconda3/etc/profile.d/conda.sh &&
    conda activate {CONDA_ENV_NAME} &&
    cd /home/texsols/QuantBio/algorithms/QFold &&
    python3 main.py "{peptide_name}" "{sequence}" {rotation_bits} "{initialization}" "{mode}" > "{output_log}" 2>&1
    """

    logging.info(f"Executing QFold command:\n{command}")
    subprocess.run(command, shell=True, executable="/bin/bash")

    output_files = [f for f in os.listdir(task_output_folder) if os.path.isfile(os.path.join(task_output_folder, f))]
    file_info = []
    for output_file in output_files:
        file_type = get_file_type(output_file)
        azure_link = generate_azure_link(task_id, output_file)
        file_info.append({
            "file_name": output_file,
            "file_type": file_type,
            "azure_link": azure_link
        })

    azure_result = upload_task_outputs(task_id, task_output_folder)

    return {
        "message": "QFold processing completed",
        "task_id": task_id,
        "azure_files": azure_result.get("uploaded_files", []),
        "output_log": azure_result.get("uploaded_files", [])[0] if azure_result.get("uploaded_files") else None,
        "output_file_details": file_info
    }
