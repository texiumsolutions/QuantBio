API Reference
=============

This section provides documentation for the RESTful API endpoints implemented in the Qubio backend. These APIs expose quantum and classical bioinformatics tools as HTTP services, enabling programmatic access to core functionality.

Each endpoint supports task submission, monitoring, and result retrieval.

VQE API
-------

**POST** `/predict`  
Submits a new VQE task using a protein sequence to calculate its ground-state energy via the Variational Quantum Eigensolver algorithm.

Parameters:
- `protein_sequence`: (str) Required. Amino acid sequence of the protein.

**GET** `/check_status/<task_id>`  
Checks the status and retrieves logs/output files for a specific VQE task by `task_id`.

This endpoint uses backend logic in:

- `backend/services/vqe_service.py`
- Upload logic in `backend/utils/azure_upload.py`

➡ For usage strategy and integration details, see:  
:doc:`tasks/vqe`

---

QFold API
---------

**POST** `/predict`  
Submits a QFold task that uses quantum algorithms to predict the folded 3D structure of a peptide.

Parameters:
- `protein_sequence`: (str) Required. Linear sequence of the peptide.
- `peptide_name`: (str) Required. Identifier name.
- `rotation_bits`: (int) Optional. Rotation bit precision (default: 2).
- `initialization`: (str) Optional. Initial config (`minifold`, `random`).
- `mode`: (str) Optional. `simulation` or `execution` (default: `simulation`).

**GET** `/check_status/<task_id>`  
Checks the folding status, retrieves logs, and returns downloadable outputs from Azure Blob Storage.

This endpoint uses:

- `backend/services/qfold_service.py`
- Upload logic in `backend/utils/azure_upload.py`

➡ For use-case explanations and strategic motivations, refer to:  
:doc:`tasks/qfold`
