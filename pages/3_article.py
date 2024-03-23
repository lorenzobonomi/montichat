## Article page

# Libraries
import streamlit as st

# App functions
from data import loadFile

fileName = 'article'

st.set_page_config(page_title = fileName)

st.markdown(f'### Sales dataset {fileName}')
st.sidebar.header(f"{fileName}")
st.write(f'''Read the {fileName} and evaluate montiChat skills''')

article = loadFile(fileName)
st.markdown(article)