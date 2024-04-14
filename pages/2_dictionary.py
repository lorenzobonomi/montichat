#### Article page

### Libraries
# Libraries
import streamlit as st
import re

# App functions
from data import loadFile, loadData

### General settings
# Load dictionary
fileName = 'dictionary'
dictionary = loadFile(fileName)

# Get names of features from session variable
featuresNames = st.session_state.get('features')

# Find features names and make text bold
regex_pattern = r"\b(" + "|".join(featuresNames) + r")\b"
dictionaryBold = re.sub(regex_pattern, r"**\1**", dictionary)


##  Streamlit Page
st.set_page_config(page_title = fileName)

# Sidebar
st.sidebar.header(f"{fileName}")

# Show dictionary
st.markdown(f'### Sales dataset {fileName}')
st.write("")
st.markdown(dictionaryBold)