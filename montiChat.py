### montiChat App

## montiChat page

# Libraries
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import datetime


# llama libraries
from llama_index.core.tools import QueryEngineTool, ToolMetadata
from llama_index.core.query_engine import PandasQueryEngine

# App functions
from data import loadData
from agents import agentOpenAI
from data import extract_code
from data import promptChart


top_agent, base_query_engine, query_engines, all_tools = agentOpenAI()

if 'visibility' not in st.session_state:
    st.session_state.visibility = 'visible'
    st.session_state.disabled = False


st. set_page_config(page_title = 'montiChat')


with st.sidebar:

    st.header('montiChat')
    st.markdown('Play with the chatbot and the agents')

    st.header('OpenAI Chatbot')
    systemPrompt = st.text_area(
        'System Prompt', 
        value = '''You are a data scientist.
You reply with concise statements.
Do not write too much.'''
)

    #width = st.sidebar.slider("plot width", 1, 25, 3)
    #height = st.sidebar.slider("plot height", 1, 25, 1)

def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
local_css('style.css')   

st.markdown(
    """
<style>
button {
    height: auto;
    width: 10px;
    padding-top: 1px !important;
    padding-bottom: 1px !important;
}
</style>
""",
    unsafe_allow_html=True,
)


st.markdown('##### Click one prompt or ask your question in the chat')
st.text(" \n")

col1, col2 = st.columns(2)
col3, col4 = st.columns(2)

buttonList = [
    'UK quantity',
    'A trend question',
    'The dictionary',
    'Generate a chart'
]

promptList = [
    'Which is the total of quantity for United Kingdom?',
    'Which is the month with the highest value for sum of quantity for United Kingdom?',
    'Which is the definition of InvoiceNo in the dictionary?',
    'which are the top 5 countries by total sum of quantity? Generate a bar chart'
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
        {'role': 'assistant', 'content': 'Ask me a question about the data', 'chart': ''}
    ]

if 'query_engine' not in st.session_state.keys(): 
        st.session_state.query_engine = top_agent


if promptSelected1 :
    prompt = promptSelected1
    st.session_state.messages.append({'role': 'user', 'content': prompt, 'chart': ''})
    st.chat_input('Your question')

elif promptSelected2:
    prompt = promptSelected2
    st.session_state.messages.append({'role': 'user', 'content': prompt, 'chart': ''})
    st.chat_input('Your question')

elif promptSelected3:
    prompt = promptSelected3
    st.session_state.messages.append({'role': 'user', 'content': prompt, 'chart': ''})
    st.chat_input('Your question')

elif promptSelected4:
    prompt = promptSelected4
    st.session_state.messages.append({'role': 'user', 'content': prompt, 'chart': ''})
    st.chat_input('Your question')

elif prompt := st.chat_input('Your question'): 
    st.session_state.messages.append({'role': 'user', 'content': prompt, 'chart': ''})
    st.session_state.messages.append({'role': 'system', 'content' : systemPrompt, 'chart': ''})
    
for message in st.session_state.messages:
    with st.chat_message(message['role']):
        st.write(message['content'])

        if message['chart'] != '':
            st.image(message['chart'], caption = None, use_column_width = "auto")


chartNumber = len(st.session_state.messages)

if st.session_state.messages[-1]['role'] != 'assistant':
    with st.chat_message('assistant'):
        
        with st.spinner('Thinking...'):
            prompt = promptChart(prompt)
            response = st.session_state.query_engine.query(prompt)

            timeStampChartNumber = str(datetime.datetime.now()) + '_' + str(chartNumber)
            
            if codeChart := extract_code(response.response, timeStampChartNumber):
                print(chartNumber)
                plot_area = st.empty()
                #plt.rcParams['figure.figsize'] = (10, 6) 
                plot_area.pyplot(exec(codeChart))
             
                #st.image('chart.jpg', caption = None, use_column_width = "auto")

                chart = f'./charts/chart{timeStampChartNumber}.jpg'

                message = {'role': 'assistant', 'content': '', 'chart': chart}
                st.session_state.messages.append(message)
                
                
                
            else:
                st.write(response.response)  

                message = {'role': 'assistant', 'content': response.response, 'chart': ''}
                st.session_state.messages.append(message)
                
            chartNumber += 1

