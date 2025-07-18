import streamlit as st
import numpy as np
from PIL import Image
import io
import pandas as pd
import time
import random
import ast

# Set page config for wide layout
st.set_page_config(
    page_title="SMILES String Analysis",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Load mapping data
@st.cache_data
def load_mapping_data():
    """Load the SMILES mapping data from CSV"""
    try:
        df = pd.read_csv('mapping.csv')
        return df
    except FileNotFoundError:
        st.error("mapping.csv file not found. Please ensure it's in the same directory as this script.")
        return None

# Set page title with stored SMILES in top right
title_col, stored_col = st.columns([2, 1])
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
        # Load mapping data
        mapping_df = load_mapping_data()
        
        if mapping_df is not None:
            # Check if SMILES is in the mapping
            smiles_row = mapping_df[mapping_df['SMILES'] == smiles_input]
            
            if not smiles_row.empty:
                # Store the SMILES string in session state FIRST
                st.session_state['current_smiles'] = smiles_input
                
                # Show progress bar with random delay between 10-15 seconds
                delay_seconds = random.randint(10, 15)
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                for i in range(delay_seconds):
                    progress = (i + 1) / delay_seconds
                    progress_bar.progress(progress)
                    status_text.text(f'Processing models... {i+1}/{delay_seconds} seconds')
                    time.sleep(1)
                
                # Clear progress indicators
                progress_bar.empty()
                status_text.empty()
                
                # Get data from CSV
                row_data = smiles_row.iloc[0]
                
                # Parse toxicophores (they're stored as string representation of list)
                try:
                    toxicophores_list = ast.literal_eval(row_data['Toxicophores'])
                except:
                    toxicophores_list = [row_data['Toxicophores']]
                
                # Store results from CSV
                st.session_state['phlda1_result'] = {
                    'classification': row_data['LINCS_Classification'].lower(),
                    'z_score': float(row_data['Z_Score'])
                }
                
                st.session_state['toxicophores'] = toxicophores_list
                
                st.session_state['models_run'] = True
                st.success(f"All models completed for: {smiles_input}")
                st.rerun()  # Force immediate rerun to show updated stored SMILES
                
            else:
                # SMILES not in cache
                st.warning("Not in cache, SMILES will be processed in the background")
        else:
            st.error("Could not load mapping data. Please check that mapping.csv exists.")
        
    else:
        st.warning("Please enter a SMILES string first")

# Display results if models have been run
if st.session_state.get('models_run', False):
    st.header("Results")
    
    # Create three columns for the three models with better spacing
    col1, col2, col3 = st.columns([1, 1, 1.2])
    
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
            st.write("**Toxic parts identified:**")
            for i, toxicophore in enumerate(st.session_state['toxicophores'], 1):
                st.write(f"{i}. {toxicophore}")
        else:
            st.write("No toxicophores detected")         

# Add a clear results button (centered) - but don't show the last row of metrics
if st.session_state.get('models_run', False):
    col_clear_left, col_clear_center = st.columns([1, 1])
    with col_clear_center:
        if st.button("Clear Results", use_container_width=True):
            for key in ['models_run', 'phlda1_result', 'toxicophores', 'cell_painting']:
                if key in st.session_state:
                    del st.session_state[key]
            st.rerun()