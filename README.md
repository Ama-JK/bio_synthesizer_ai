# 🌿 Bio-Synthesizer AI

Bio-Synthesizer AI is a local-first analytical tool designed for botanical researchers and medicinal chemistry enthusiasts. By leveraging LangGraph for structured state-machine navigation and Ollama (Llama 3) for reasoning, this tool automates the retrieval of botanical information and chemical properties.
---

## 🏗️ Architecture Blueprint

The system orchestrates operations through a structured state-graph pipeline:

*   **Botanical Parser:** Extracts plant species names and morphological metadata from user input.
*   **PubChem Integration:** Automatically queries secure public chemical databases to fetch validated molecular structures and compound properties.
*   **Report Generation Engine:** Synthesizes the identified data into structured scientific reports.

---

## 🛠️ Tech Stack & Tooling

| Layer | Technology | Purpose |
| :--- | :--- | :--- |
| **Orchestration** | LangGraph / LangChain | Directed Acyclic Graph (DAG) for stateful agent workflows |
| **Brain Core** | Ollama / Llama 3 | Localized Private and offline LLM inference |
| **Data Fetcher** | PubChem API | Real-time retrieval of chemical/molecular data |
| **Interface** | Streamlit | Real-time monitoring and interactve web dashboard |
| **Testing** | Unittest | Automated validation of agent logic and API pipelines |
---

## 📂 Project Directory Structure

```text
├── app.py                # Streamlit Web UI
├── graph_engine.py       # LangGraph Core State Engine & Logic Nodes
├── test_ollama.py        # Automated Connectivity Tests for Local LLM
├── test_pubchem.py       # API Validation suite for Chemical Data
└── README.md             # Project documentation

---
```
## Installation & Local Execution
## 1. Clone the repository & Setup
```bash
git clone https://github.com/Ama-JK/bio_synthesizer_ai.git
cd bio_synthesizer_ai
pip install -r requirements.txt
```

## 2. Boot up local LLM
Ensure Ollama is installed and running the Llama 3 model:
```bash
ollama run llama3
```

## 3. Validate Environment
Run the test scripts to ensure your pipeline is correctly configured:
```bash
python test_ollama.py
python test_pubchem.py
```

## 4. Fire up UI 
```bash
streamlit run app.py
```
