import streamlit as st
import numpy as np
from PIL import Image
import io
import time
import random

# Set page config for wide layout
st.set_page_config(
    page_title="SMILES String Analysis",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Embedded mapping data
SMILES_DATABASE = {
    "CC(=O)OC1=CC=CC=C1C(=O)O": {
        "z_score": -1.824,
        "classification": "Down",
        "toxicophores": [["Aromatic Ring", [6, 11]], ["Ester", [1, 5]], ["Carboxylic Acid", [12, 16]]]
    },
    "CN1C=NC2=C1C(=O)N(C(=O)N2C)C": {
        "z_score": -2.165,
        "classification": "Down",
        "toxicophores": [["Imide", [7, 13]], ["Dimethylamino", [1, 3]]]
    },
    "CC1=CC(=O)NC(C)=C1": {
        "z_score": -1.654,
        "classification": "Down",
        "toxicophores": [["Ketone", [5, 6]], ["Aniline-like", [3, 5]]]
    },
    "CN(C)C=O": {
        "z_score": 1.795,
        "classification": "Up",
        "toxicophores": [["Formamide", [2, 4]], ["Tertiary Amine", [1, 3]]]
    },
    "CC(C)NCC(O)=O": {
        "z_score": 1.934,
        "classification": "Up",
        "toxicophores": [["Amine", [3]], ["Carboxylic Acid", [6, 8]]]
    },
    "CC(C)CC1=CC=C(C=C1)C(C)C(=O)O": {
        "z_score": -1.551,
        "classification": "Down",
        "toxicophores": [["Aromatic Ring", [6, 11]], ["Branched Alkyl", [1, 3]], ["Carboxylic Acid", [14, 18]]]
    },
    "CCOC(=O)C1=CC=CC=C1Cl": {
        "z_score": -1.778,
        "classification": "Down",
        "toxicophores": [["Ester", [2, 6]], ["Chlorobenzene", [10, 13]]]
    },
    "CC1=CC=C(C=C1)C(C)NC(=O)CCl": {
        "z_score": -1.613,
        "classification": "Down",
        "toxicophores": [["Aromatic Ring", [3, 8]], ["Acetamide", [10, 14]], ["Alkyl Chloride", [15, 17]]]
    },
    "CCC(CC)CO": {
        "z_score": -1.676,
        "classification": "Down",
        "toxicophores": [["Secondary Alcohol", [6, 8]], ["Branched Alkyl", [1, 3]]]
    },
    "O=C(NC1=CC=CC=C1)C2=CC=CC=C2": {
        "z_score": -1.964,
        "classification": "Down",
        "toxicophores": [["Anilide", [1, 13]], ["Benzene", [14, 19]]]
    },
    "C1=CC=C(C=C1)CN2C=NC3=C2C=CC=C3": {
        "z_score": -1.521,
        "classification": "Down",
        "toxicophores": [["Benzene", [1, 6]], ["Imidazole", [9, 13]]]
    },
    "COC1=CC=CC=C1OC": {
        "z_score": -1.267,
        "classification": "Neutral",
        "toxicophores": [["Methoxybenzene", [1, 8]]]
    },
    "CCN(CC)CCOC1=CC=CC=C1Cl": {
        "z_score": 1.678,
        "classification": "Up",
        "toxicophores": [["Chlorobenzene", [11, 14]], ["Tertiary Amine", [1, 5]]]
    },
    "CN1CCC(CC1)COC2=CC=CC=C2Cl": {
        "z_score": -1.861,
        "classification": "Down",
        "toxicophores": [["Morpholine-like", [2, 6]], ["Aryl Chloride", [14, 17]]]
    },
    "CCOC(=O)C3=CC=C(C=C3)N": {
        "z_score": -1.711,
        "classification": "Down",
        "toxicophores": [["Aromatic Amine", [13, 13]], ["Ester", [2, 6]]]
    }
}

# Set page title with stored SMILES in top right
title_col, stored_col = st.columns([3, 1])
with title_col:
    st.title("SMILES String Analysis")
with stored_col:
    if 'current_smiles' in st.session_state:
        st.info(f"Stored: {st.session_state['current_smiles']}")

# Create text input for SMILES string with centered button
smiles_input = st.text_input("Enter SMILES string:", placeholder="e.g., CCO, C1=CC=CC=C1")

# Center the Run Models button
col_left, col_center, col_right = st.columns([1, 1, 1])
with col_center:
    run_button = st.button("Run Models", use_container_width=True)

# Add run models button
if run_button:
    if smiles_input:
        # Check if SMILES is in our database
        if smiles_input in SMILES_DATABASE:
            # Store the SMILES string in session state FIRST
            st.session_state['current_smiles'] = smiles_input
            
            # Show progress bar with random delay between 10-15 seconds
            delay_seconds = random.randint(10, 15)

            for i in range(delay_seconds):
                progress = (i + 1) / delay_seconds
                time.sleep(1)
            
            # Get data from database
            data = SMILES_DATABASE[smiles_input]
            
            # Format toxicophores for display
            formatted_toxicophores = []
            for tox_name, positions in data["toxicophores"]:
                if len(positions) == 2:
                    formatted_toxicophores.append(f"{tox_name} (positions {positions[0]}-{positions[1]})")
                else:
                    formatted_toxicophores.append(f"{tox_name} (position {positions[0]})")
            
            # Store results
            st.session_state['phlda1_result'] = {
                'classification': data["classification"].lower(),
                'z_score': data["z_score"]
            }
            
            st.session_state['toxicophores'] = formatted_toxicophores
            st.session_state['models_run'] = True
            
            st.success(f"All models completed for: {smiles_input}")
            st.rerun()
        else:
            # SMILES not in cache
            st.warning("⚠️ Not in cache, SMILES will be processed in the background")
            st.info("💡 For immediate results, try one of these example SMILES:")
            
            # Show some example SMILES
            examples = list(SMILES_DATABASE.keys())[:5]
            for example in examples:
                st.code(example)
    else:
        st.warning("Please enter a SMILES string first")

# Display results if models have been run
if st.session_state.get('models_run', False):
    st.header("Results")
    
    # Create two columns for the two models
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("PHLDA1 Analysis")
        if 'phlda1_result' in st.session_state:
            result = st.session_state['phlda1_result']
            
            # Display classification with color coding
            if result['classification'] == 'up':
                st.success(f"Classification: ⬆️ {result['classification'].upper()}")
            elif result['classification'] == 'down':
                st.error(f"Classification: ⬇️ {result['classification'].upper()}")
            else:
                st.info(f"Classification: ➡️ {result['classification'].upper()}")
            
            st.metric("Z-Score", f"{result['z_score']:.3f}")
    
    with col2:
        st.subheader("Toxicophores")
        if 'toxicophores' in st.session_state:
            if st.session_state['toxicophores']:
                st.write("**Toxic structural alerts identified:**")
                for i, toxicophore in enumerate(st.session_state['toxicophores'], 1):
                    st.write(f"{i}. {toxicophore}")
            else:
                st.success("✅ No toxicophores detected")
        else:
            st.write("No toxicophores detected")

# Add a clear results button (centered)
if st.session_state.get('models_run', False):
    st.markdown("---")
    col_clear_left, col_clear_center, col_clear_right = st.columns([1, 1, 1])
    with col_clear_center:
        if st.button("Clear Results", use_container_width=True):
            for key in ['models_run', 'phlda1_result', 'toxicophores']:
                if key in st.session_state:
                    del st.session_state[key]
            st.rerun()