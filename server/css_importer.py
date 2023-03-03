import os
import streamlit as st

# Adding styles
script_dir = os.path.dirname(__file__)

def local_css(file_name):
    abs_path_dir = os.path.join(script_dir, file_name)
    with open(abs_path_dir) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)