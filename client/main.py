import os
import sys
from PIL import Image
import streamlit as st

favicon = Image.open("client/assets/paper.ico")
logo = Image.open("client/assets/paper.png")

st.set_page_config(page_title="Paper.sum", page_icon=favicon)
st.image(logo, caption='', width=100)
st.title("Paper.sum")

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from server.main import Generate_summary
from components import Generate_Components
from sampledata import sample

from css_importer import local_css
local_css("style.css")

link = st.text_input("Input arxiv URL to Research Paper", placeholder="https://arxiv.org/abs/1512.03385")
selectable_tags = ['Experiments and Results', 'Proposed solution', 'Building blocks and Methalogy']
default_tags = ['Experiments and Results']
selected_tags = st.multiselect(
    'Select tags',
    selectable_tags, default_tags, max_selections=1)

if link:
    if st.button('Summarize'):
        with st.spinner("Reading..."):
            summary = Generate_summary(link, selected_tags)
        Generate_Components(summary)
    else:
        st.markdown('### Click on summarize to generate')
