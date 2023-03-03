import streamlit as st
st.set_page_config(page_title="Paper.sum", page_icon=":page_facing_up:")
st.title("Paper.sum")

from main import Generate_summary
from components import Generate_Components
from sampledata import sample

from css_importer import local_css
local_css("style.css")

link = st.text_input("Input URL to Research Paper")
selectable_tags = ['Experiments', 'Results', 'Beginner']
default_tags = ['Experiments']
selected_tags = st.multiselect(
    'Select tags',
    selectable_tags, default_tags)

if link:
    if st.button('Summarize'):
        summary = Generate_summary(link, selected_tags)
        Generate_Components(summary)
    else:
        st.markdown('### Click on summarize to generate')
