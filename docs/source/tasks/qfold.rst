QFold Task Integration
======================

QFold is a quantum-inspired approach for predicting protein folding by encoding structural constraints into a Hamiltonian and minimizing it via quantum algorithms. The API exposes this functionality to end-users and developers via an intuitive REST interface.

Use Case in Qubio
-----------------

Protein folding is a foundational challenge in structural biology. QFold complements modern tools like AlphaFold by:

- Generating initial low-energy conformations
- Modeling small therapeutic peptides
- Predicting how point mutations affect folding

How We Use It
-------------

- **Input**: Users submit sequence and task configurations via the `/predict` endpoint.
- **Quantum Optimization**: The Hamiltonian encoding the folding landscape is optimized using VQE/QAOA-style methods.
- **Output**: The result includes predicted structure, log traces, and download links from Azure Blob Storage.

Why QFold via API?
------------------

Exposing QFold as a backend service:

- Enables **automation** in structural prediction pipelines.
- Supports **remote quantum execution** and **simulations**.
- Offers **flexibility** via input flags (`mode`, `rotation_bits`, etc.).

Scientific Significance
------------------------

Integrating QFold as an API aligns with our long-term goal to embed quantum-augmented modeling tools into broader bioinformatics platforms. This includes:

- Quantum-assisted peptide design
- Preprocessing for AlphaFold/Rosetta workflows
- Structure-based drug screening using predicted folds
