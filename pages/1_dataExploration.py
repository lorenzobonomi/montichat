## Data Exploration page to double check chatbot answers

# Libraries
import streamlit as st
import altair as alt
import pandas as pd

# App functions
from data import loadData


if 'visibility' not in st.session_state:
    st.session_state.visibility = 'visible'
    st.session_state.disabled = False

# Load data and list of countries for slicer
fileName = 'salesData'
data = loadData(fileName)
listOfCountries = data['Country'].unique().tolist()

# Streamlit page settings
st.set_page_config(layout = 'wide', page_title = 'Data Exploration')
st.markdown('### Data Exploration')

# Sidbar with countries slicer
with st.sidebar.header("Data Exploration"):
    st.write(
    """Check the data and select the Country"""
)
    country = st.selectbox(
    "Select the country:",
    (listOfCountries),
    label_visibility=st.session_state.visibility,
    disabled=st.session_state.disabled,
)
    
# Data transformations and grouping for chart
dataBarchart = data \
    .groupby('Country', as_index = False)['Quantity'] \
    .sum() \
    .sort_values(by = 'Quantity', ascending = False) \
    .head(30)

dataCountry = data[data['Country'] == country]
dataCountry['InvoiceDate'] = pd.to_datetime(dataCountry['InvoiceDate'])

dataTimeChart = dataCountry \
    .groupby(pd.Grouper(key = 'InvoiceDate', freq = 'M'))['Quantity'] \
    .sum() \
    .reset_index() \

# Charts and tables
col1, col2, col3  = st.columns(3)
col1.metric('Number of rows', ('{}'.format(round(dataCountry.shape[0], 0))))
col2.metric('Number of Customers', ('{}'.format(round(dataCountry['CustomerID'].nunique(), 0))))
col3.metric('Average UnitPrice', ('{}'.format(round(dataCountry['UnitPrice'].mean(), 2))))

st.dataframe(data = dataCountry)
st.write(alt.Chart(dataTimeChart)
            .mark_line()
            .encode(
                x = 'InvoiceDate',
                y = 'Quantity'
            )
)

st.write(alt.Chart(dataBarchart)
            .mark_bar()
            .encode(y = alt.Y('Country', sort = None), x = 'Quantity')
)