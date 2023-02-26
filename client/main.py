import streamlit as st
import os

st.set_page_config(page_title="SummarizeIt", page_icon=":page_facing_up:")
st.title("Summarize it")

# Adding styles
script_dir = os.path.dirname(__file__)
def local_css(file_name):
    abs_path_dir = os.path.join(script_dir, file_name)
    with open(abs_path_dir) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
local_css("style.css")

st.text_input("Input URL to Research Paper")
selectable_tags = ['Beginner', 'Sample Tag', 'Tag2', 'Tag3']
default_tags = ['Beginner']
tags = st.multiselect(
    'Select tags',
    selectable_tags, default_tags)
