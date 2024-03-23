### montiChat App

## montiChat page

# Librariesß
import streamlit as st
import pandas as pd

# llama libraries
from llama_index.core.tools import QueryEngineTool, ToolMetadata
from llama_index.core.query_engine import PandasQueryEngine

# App functions
from data import loadData
from agents import agentOpenAI


top_agent, base_query_engine, query_engines, all_tools = agentOpenAI()

if 'visibility' not in st.session_state:
    st.session_state.visibility = 'visible'
    st.session_state.disabled = False


st. set_page_config(layout = 'wide', page_title = 'multiApp')

with st.sidebar:

    st.header('montiChat')
    st.markdown('Play with the chatbot and the agents')

def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
local_css('style.css')   

st.markdown('##### Click one prompt or ask your question in the chat')
st.text(" \n")
col1, col2, col3, col4 = st.columns(4)

buttonList = [
    'Ask about UK quantity',
    'Ask a trend question',
    'Ask about the dictionary',
    'Ask about the article'
]

promptList = [
    'Which is the total of quantity for United Kingdom?',
    'Which is the month with the highest value for sum of quantity for United Kingdom?',
    'Which is the definition of InvoiceNo in the dictionary?',
    'Summarize the article'
]


with col1:
    if st.button(buttonList[0]):
        promptSelected1 = promptList[0]
    else:
        promptSelected1 = None

with col2:
    if st.button(buttonList[1]):
        promptSelected2 = promptList[1]
    else:
        promptSelected2 = None

with col3:
    if st.button(buttonList[2]):
        promptSelected3 = promptList[2]
    else:
        promptSelected3 = None

with col4:
    if st.button(buttonList[3]):
        promptSelected4 = promptList[3]
    else:
        promptSelected4 = None

if 'messages' not in st.session_state.keys():
    st.session_state.messages = [
        {'role': 'assistant', 'content': 'Ask me a question about the data'}
    ]

if 'query_engine' not in st.session_state.keys(): 
        st.session_state.query_engine = top_agent


if promptSelected1 :
    prompt = promptSelected1
    st.session_state.messages.append({'role': 'user', 'content': prompt})
elif promptSelected2:
    prompt = promptSelected2
    st.session_state.messages.append({'role': 'user', 'content': prompt})
elif promptSelected3:
    prompt = promptSelected3
    st.session_state.messages.append({'role': 'user', 'content': prompt})
elif promptSelected4:
    prompt = promptSelected4
    st.session_state.messages.append({'role': 'user', 'content': prompt})
elif prompt := st.chat_input('Your question'): 
    st.session_state.messages.append({'role': 'user', 'content': prompt})
    
for message in st.session_state.messages:
    with st.chat_message(message['role']):
        st.write(message['content'])

if st.session_state.messages[-1]['role'] != 'assistant':
    with st.chat_message('assistant'):
        
        with st.spinner('Thinking...'):
            response = st.session_state.query_engine.query(prompt)
            st.write(response.response)
            message = {'role': 'assistant', 'content': response.response}
            st.session_state.messages.append(message)






