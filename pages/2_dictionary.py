## Article page

# Libraries
import streamlit as st

# App functions
from data import loadFile

fileName = 'dictionary'

st.set_page_config(page_title = fileName)

st.markdown(f'### Sales dataset {fileName}')
st.sidebar.header(f"{fileName}")
st.write(f'''{fileName} of the sales dataset''')

dictionary = loadFile(fileName)
st.markdown(dictionary)