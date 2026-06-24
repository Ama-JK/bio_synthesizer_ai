import streamlit as st
import uuid
from graph_engine import start_pipeline, resume_pipeline

# Streamlit Page configuration
st.set_page_config(page_title="Bio-Synthesizer AI", page_icon="🌿", layout="centered")
st.title("🌿 Bio-Synthesizer (Human-in-the-Loop)")
st.write("Analyze plants with real-time chemical tracking and human approval controls.")

# Initializing Session States to handle LangGraph checkpoints
if "thread_id" not in st.session_state:
    st.session_state["thread_id"] = str(uuid.uuid4())
if "step" not in st.session_state:
    st.session_state["step"] = "input"
if "graph_data" not in st.session_state:
    st.session_state["graph_data"] = {}

# ----------------------------------------------------
# STEP 1: Get Plant Input from User
# ----------------------------------------------------
if st.session_state["step"] == "input":
    plant_input = st.text_input("Enter Plant Name (e.g., Curry leaves, Tulsi, Neem):", "")
    
    if st.button("Fetch Data 🚀"):
        if plant_input.strip():
            with st.spinner("🧠 Specimen & PubChem Agents are working... Please wait..."):
                
                # Reset Trick: Clear previous graph data and create a new thread_id on every fresh click
                st.session_state["graph_data"] = {} 
                st.session_state["thread_id"] = str(uuid.uuid4()) 
                
                # Start the pipeline with the newly generated thread ID
                result = start_pipeline(plant_input, st.session_state["thread_id"])
                
                st.session_state["graph_data"] = result
                st.session_state["step"] = "approval"
                st.rerun()
        else:
            st.warning("Please enter a valid plant name first!")

# ----------------------------------------------------
# STEP 2: Human-in-the-Loop Approval Screen 🚦
# ----------------------------------------------------
elif st.session_state["step"] == "approval":
    data = st.session_state["graph_data"]
    thread_id = st.session_state["thread_id"]
    
    st.success("✅ Part 1 Complete! Data fetched successfully.")
    st.subheader("🧪 Phytochemical Verification")
    
    st.markdown(f"**Searched Plant Input:** `{data.get('plant_name', 'N/A').upper()}`")
    st.markdown(f"**Identified Chemical:** `{data.get('chemical_name', 'N/A').upper()}`")
    st.markdown(f"**Molecular Formula:** `{data.get('molecular_formula', 'N/A')}`")
    st.markdown(f"**IUPAC Name:** `{data.get('iupac_name', 'N/A')}`")
    
    st.divider()
    st.warning("🤖 **Human Intervention Required:** Should the Scientist Agent proceed to generate a medical report?")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("✅ Approve & Run Scientist Agent", type="primary"):
            with st.spinner("🧠 Scientist Agent is generating report via Ollama..."):
                # Resume the graph execution with approved status
                final_result = resume_pipeline(thread_id, "approved")
                st.session_state["graph_data"] = final_result
                st.session_state["step"] = "final"
                st.rerun()
                
    with col2:
        if st.button("❌ Reject & Stop Workflow"):
            # Resume the graph execution with rejected status
            final_result = resume_pipeline(thread_id, "rejected")
            st.session_state["graph_data"] = final_result
            st.session_state["step"] = "final"
            st.rerun()

# ----------------------------------------------------
# STEP 3: Final Output Screen
# ----------------------------------------------------
elif st.session_state["step"] == "final":
    data = st.session_state["graph_data"]
    
    # Adding a dashboard summary of the entire pipeline data
    st.success("🎉 Analysis Complete!")
    
    st.subheader("📊 Analysis Summary Dashboard")
    
    # Using columns to display data
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"**🌿 Original Plant Input:** `{data.get('plant_name', 'N/A').upper()}`")
        st.markdown(f"**🧪 Identified Chemical:** `{data.get('chemical_name', 'N/A').upper()}`")
    with col2:
        st.markdown(f"**🔬 Molecular Formula:** `{data.get('molecular_formula', 'N/A')}`")
        st.markdown(f"**🧬 IUPAC Name:** `{data.get('iupac_name', 'N/A')}`")
    
    st.divider()
    st.subheader("🔬 Final Scientist Agent Report")
    st.write(data.get("scientific_report", "No report available."))
   
    st.divider()
    if st.button("🔄 Analyze Another Specimen"):
        # Reset everything back to the initial input screen
        st.session_state["step"] = "input"
        st.session_state["graph_data"] = {}
        st.session_state["thread_id"] = str(uuid.uuid4())
        st.rerun()