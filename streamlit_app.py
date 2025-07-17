import streamlit as st
import numpy as np
from PIL import Image
import io

# Set page config for wide layout
st.set_page_config(
    page_title="SMILES String Analysis",
    layout="wide",
    initial_sidebar_state="collapsed"
)

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
        # Store the SMILES string in session state FIRST
        st.session_state['current_smiles'] = smiles_input
        st.session_state['models_run'] = True
        
        # Generate placeholder results - replace with actual model calls
        st.session_state['phlda1_result'] = {
            'classification': np.random.choice(['up', 'down']),
            'z_score': np.random.normal(0, 1)
        }
        
        st.session_state['toxicophores'] = [
            "Benzene ring (position 1-6)",
            "Hydroxyl group (position 7)",
            "Methyl group (position 8-10)"
        ]
        
        # Placeholder for cell painting image
        st.session_state['cell_painting'] = {
            'image_generated': True,
            'info': {
                'cell_viability': '85%',
                'morphology_score': 0.73,
                'treatment_response': 'Moderate'
            }
        }
        
        st.success(f"All models completed for: {smiles_input}")
        st.rerun()  # Force immediate rerun to show updated stored SMILES
        
    else:
        st.warning("Please enter a SMILES string first")

# Display results if models have been run
if st.session_state.get('models_run', False):
    st.header("Results")
    
    # Create three columns for the three models with better spacing
    col1, col2, col3 = st.columns([1, 1, 1.2])
    
    with col1:
        st.subheader("🧬 PHLDA1 Analysis")
        if 'phlda1_result' in st.session_state:
            result = st.session_state['phlda1_result']
            
            # Display classification with color coding
            if result['classification'] == 'up':
                st.success(f"Classification: ⬆️ {result['classification'].upper()}")
            else:
                st.error(f"Classification: ⬇️ {result['classification'].upper()}")
            
            st.metric("Z-Score", f"{result['z_score']:.3f}")
    
    with col2:
        st.subheader("☠️ Toxicophores")
        if 'toxicophores' in st.session_state:
            st.write("**Toxic parts identified:**")
            for i, toxicophore in enumerate(st.session_state['toxicophores'], 1):
                st.write(f"{i}. {toxicophore}")
        else:
            st.write("No toxicophores detected")
    
    with col3:
        st.subheader("🔬 Cell Painting")
        if 'cell_painting' in st.session_state:
            cell_data = st.session_state['cell_painting']
            
            # Placeholder for image - replace with actual image generation
            if cell_data['image_generated']:
                st.write("**Cell Painting Image:**")
                # Create a placeholder image
                img_array = np.random.rand(200, 200, 3)
                img = Image.fromarray((img_array * 255).astype(np.uint8))
                st.image(img, caption="Cell painting visualization", width=250)
            
            st.write("**Cell Painting Metrics:**")
            
            # Nuclei count with tooltip
            st.metric("Nuclei Count", "1,247", 
                     help="Number of nuclei objects per well (Cells_Number_Object_Number) - indicates cell density and proliferation")
            
            # Nuclear features
            col3a, col3b = st.columns(2)
            with col3a:
                st.metric("Nuclear Area", "245.6 μm²", 
                         help="pyMorph feature: Average nuclear area measurement indicating cell size and health")
            with col3b:
                st.metric("Nuclear Eccentricity", "0.73", 
                         help="pyMorph feature: Shape measurement (0=circle, 1=line) indicating nuclear morphology changes")
            
            # Mitochondrial features
            col3c, col3d = st.columns(2)
            with col3c:
                st.metric("Mito Texture", "8.42", 
                         help="Mitochondrial texture measurement from Mito channel - indicates mitochondrial organization")
            with col3d:
                st.metric("Mito Intensity Var", "12.7", 
                         help="Mitochondrial intensity variance from Mito channel - indicates mitochondrial health/distribution")
            
            # Micronuclei frequency
            st.metric("Micronuclei Freq", "2.3%", 
                     help="Frequency of small Hoechst-positive objects indicating DNA damage and chromosomal instability")
            
            # LysoTracker/LipidTOX intensities
            col3e, col3f = st.columns(2)
            with col3e:
                st.metric("LysoTracker", "156.8", 
                         help="LysoTracker intensity from CP AGP/Lysosome channel - indicates lysosomal activity")
            with col3f:
                st.metric("LipidTOX", "89.3", 
                         help="LipidTOX intensity from CP AGP/Lysosome channel - indicates lipid accumulation/metabolism")

# Add a clear results button (centered)
if st.session_state.get('models_run', False):
    col_clear_left, col_clear_center, col_clear_right = st.columns([1, 1, 1])
    with col_clear_center:
        if st.button("Clear Results", use_container_width=True):
            for key in ['models_run', 'phlda1_result', 'toxicophores', 'cell_painting']:
                if key in st.session_state:
                    del st.session_state[key]
            st.rerun()