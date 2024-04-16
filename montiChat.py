#### montiChat App

### Libraries
# Libraries
import streamlit as st
import datetime
import pandas as pd

# App functions
from agents import agentOpenAI
from data import extract_code, promptChart, loadData


### Streamlit page

## General Settings
# Turn of matplotlib.pyplot warning
st.set_option('deprecation.showPyplotGlobalUse', False)
st. set_page_config(page_title = 'montiChat')


# Load dataSet
dataPandas = loadData('SalesData')
features = dataPandas.columns.tolist()

# Define session level variables
if 'dataPandas' not in st.session_state or 'features' not in st.session_state:
    st.session_state['dataPandas'] = dataPandas
    st.session_state['features'] = features

if 'visibility' not in st.session_state:
    st.session_state.visibility = 'visible'
    st.session_state.disabled = False

# Call for agents
top_agent, base_query_engine, query_engines, all_tools = agentOpenAI()


## Sidebar
with st.sidebar:

    # System prompt 
    
    systemPrompt = st.text_area(
        label = '#### System Prompt',
        value = '''You are a data scientist.
You reply with concise statements.
Do not write too much.'''
)

    # Features names:
    st.markdown('#### Dataset columns')

    for feature in features:
        st.markdown(f'##### &nbsp;&nbsp;{feature}')


## Defaults prompt buttons
# Style for prompts buttons
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

# Buttons
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

promptVariable = "promptSelected"
promptSelection = {}
col = [col1, col2, col3, col4]

## Chat session
# Prompt selection
for i in range(1, len(promptList)+1):

    with col[i-1]:
        if st.button(buttonList[i-1]):
            promptSelection[promptVariable + str(i)] = promptList[i-1]
        else:
            promptSelection[promptVariable + str(i)] = promptList[i-1] = None

      
# Define message structure. Chart is empty for non chart related answers
if 'messages' not in st.session_state.keys():
    st.session_state.messages = [
        {'role': 'assistant', 'content': 'Ask me a question about the data', 'chart': ''}
    ]

if 'query_engine' not in st.session_state.keys(): 
        st.session_state.query_engine = top_agent


for value in promptSelection.values():

    if value is not None:
        promptSelected = value
        break

    else:
        promptSelected = None


if promptSelected is not None:
    prompt = promptSelected
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


# Variable for increasing the chart number 
chartNumber = len(st.session_state.messages)

# Chatbot interaction
if st.session_state.messages[-1]['role'] != 'assistant':
    with st.chat_message('assistant'):
        
        with st.spinner('Thinking...'):
            prompt = promptChart(prompt)
            response = st.session_state.query_engine.query(prompt)

            # Varialbe for saving charts with timestamp and incremental number
            timeStampChartNumber = str(datetime.datetime.now()) + '_' + str(chartNumber)
            
            # If there's code for a chart in the answer, show it in the stream
            if codeChart := extract_code(response.response, timeStampChartNumber):
                plot_area = st.empty()
                plot_area.pyplot(exec(codeChart))

                # Chart name saved in the stream to be loaded for previous answers
                chart = f'./charts/chart{timeStampChartNumber}.jpg'
                message = {'role': 'assistant', 'content': '', 'chart': chart}
                st.session_state.messages.append(message)
                
            else:
                st.write(response.response)  
                message = {'role': 'assistant', 'content': response.response, 'chart': ''}
                st.session_state.messages.append(message)
                

