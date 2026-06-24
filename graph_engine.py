import requests
from typing import TypedDict
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver

# Define Graph State
class AgentState(TypedDict):
    plant_name: str
    chemical_name: str
    molecular_formula: str
    iupac_name: str
    scientific_report: str
    approval_status: str

# NODE 1: Plant Specimen Agent (Ollama Intelligence )
def plant_specimen_agent(state: AgentState):
    plant = state['plant_name'].strip()
    print(f"\n[Agent 1] 🌿 Specimen Agent asking Ollama for the main chemical of: {plant}")
    
    url = "http://localhost:11434/api/generate"
    prompt = f"""
    You are an expert botanical chemist and pharmacognosist. 
    The user might provide a plant name in English, or a romanized regional Indian name (e.g., Tamil, Hindi, Telugu names like 'Athimathuram', 'Tulsi', 'Inji').
    
    Step 1: Identify the actual scientific plant being referred to. (e.g., 'Athimathuram' refers to Liquorice / Glycyrrhiza glabra).
    Step 2: Find the single most primary active phytochemical (chemical compound) of that plant.
    
    Respond with ONLY the name of that primary chemical compound. Do not write explanations, introduction, punctuation, or sentences. Just one word or compound name.
    
    Example Input: Turmeric
    Example Output: curcumin
    
    Example Input: Athimathuram
    Example Output: glycyrrhizin
    
    Input: {plant}
    Output:
    """
    payload = {"model": "llama3", "prompt": prompt, "stream": False}
    
    try:
        response = requests.post(url, json=payload)
        raw_chemical = response.json().get("response", plant).strip()
        chemical = raw_chemical.split("\n")[-1].split(":")[-1].replace(".", "").replace('"', '').replace("'", "").strip().lower()
        print(f"[Agent 1] 🤖 Ollama identified primary chemical: '{chemical}'")
        return {"plant_name": plant, "chemical_name": chemical, "approval_status": "pending"}
    except Exception as e:
        print(f"[Agent 1]  Ollama failed: {e}")
        return {"plant_name": plant, "chemical_name": plant.lower(), "approval_status": "pending"}

# NODE 2: PubChem API Agent
def pubchem_api_agent(state: AgentState):
    chemical = state['chemical_name']
    print(f"\n[Agent 2]  PubChem Agent searching for: {chemical}")
    
    url = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/{chemical}/property/IUPACName,MolecularFormula/JSON"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            properties = response.json()["PropertyTable"]["Properties"][0]
            return {
                "molecular_formula": properties.get("MolecularFormula", "N/A"),
                "iupac_name": properties.get("IUPACName", "N/A")
            }
        print(f"[Agent 2]  Data not found on PubChem for: {chemical}")
        return {"molecular_formula": "N/A", "iupac_name": "N/A"}
    except Exception as e:
        print(f"[Agent 2]  API Error: {e}")
        return {"molecular_formula": "N/A", "iupac_name": "N/A"}

# NODE 3: Scientist Agent (Ollama Deep Clinical Report 🔬)
def drug_mapper_agent(state: AgentState):
    if state.get("approval_status") != "approved":
        print("\n[Agent 3]  Report Generation Rejected by User.")
        return {"scientific_report": " Report Generation Rejected by User."}
        
    print(f"\n[Agent 3] 🧠 Scientist Agent running Deep Clinical Medical Reasoning...")
    url = "http://localhost:11434/api/generate"
    
    prompt = f"""
    You are an expert Clinical Pharmacologist and Medicinal Chemist.
    Analyze the following phytochemical data and provide a formal, structured Medical & Scientific Report:
    
    Chemical Compound: {state['chemical_name']}
    Molecular Formula: {state['molecular_formula']}
    IUPAC Name: {state['iupac_name']}
    
    Please structure your response with these exact headings:
    1. CLINICAL THERAPEUTIC INDICATION (What medical conditions does it treat?)
    2. MOLECULAR MECHANISM OF ACTION (How does it interact at a cellular/enzymatic level in the human body?)
    3. PHARMACOLOGICAL INSIGHTS & BIOAVAILABILITY (Any specific scientific constraints or drug delivery challenges?)
    
    Keep the language highly professional and clinical.
    """
    payload = {"model": "llama3", "prompt": prompt, "stream": False}
    try:
        response = requests.post(url, json=payload)
        return {"scientific_report": response.json().get("response", "No report generated.")}
    except Exception as e:
        return {"scientific_report": f"Ollama Error: {e}"}

# ====================================================
# BUILD WORKFLOW GRAPH (The missing definitions are back!)
# ====================================================
workflow = StateGraph(AgentState)
workflow.add_node("SpecimenAgent", plant_specimen_agent)
workflow.add_node("PubChemAgent", pubchem_api_agent)
workflow.add_node("ScientistAgent", drug_mapper_agent)

workflow.set_entry_point("SpecimenAgent")
workflow.add_edge("SpecimenAgent", "PubChemAgent")
workflow.add_edge("PubChemAgent", "ScientistAgent")
workflow.add_edge("ScientistAgent", END)

# Memory for Human-in-the-Loop Checkpointing
memory = MemorySaver()

# # type: ignore avoids VS Code yellow linting warning lines
app_graph = workflow.compile(checkpointer=memory, interrupt_before=["ScientistAgent"]) # type: ignore

# Helper functions for Streamlit app.py
def start_pipeline(user_plant_input, thread_id):
    config = {"configurable": {"thread_id": thread_id}}
    initial_input = {"plant_name": user_plant_input}
    return app_graph.invoke(initial_input, config)

def resume_pipeline(thread_id, user_choice):
    config = {"configurable": {"thread_id": thread_id}}
    app_graph.update_state(config, {"approval_status": user_choice})
    return app_graph.invoke(None, config)