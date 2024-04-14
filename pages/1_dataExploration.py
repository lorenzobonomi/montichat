#### Data Exploration page to double check chatbot answers

### Libraries
# Libraries
import streamlit as st
import altair as alt
import pandas as pd

# App functions
from data import loadData


### Streamlit page

## General Settings
# Load data and list of countries for slicer
fileName = 'salesData'
data = loadData(fileName)


listOfCountries = data['Country'].unique().tolist()


# Streamlit page settings
if 'visibility' not in st.session_state:
    st.session_state.visibility = 'visible'
    st.session_state.disabled = False

st.set_page_config(layout = 'wide', page_title = 'Data Exploration')
st.markdown('### Data Exploration')


## Sidbar with countries slicer
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


## Data transformations
dataBarchart = data \
    .groupby('Country', as_index = False)['Quantity'] \
    .sum() \
    .sort_values(by = 'Quantity', ascending = False) \
    .head(30)

# Filter on country select 
dataCountry = data[data['Country'] == country]

# Data for time series
dataTimeChart = dataCountry \
    .groupby(pd.Grouper(key = 'InvoiceDate', freq = 'M'))['Quantity'] \
    .sum() \
    .reset_index() \

## Charts and tables

# KPI cards
st.write("")
col1, col2, col3  = st.columns(3)
col1.metric('Number of rows', ('{:,}'.format(round(dataCountry.shape[0], 0))))
col2.metric('Number of Customers', ('{:,}'.format(round(dataCountry['CustomerID'].nunique(), 0))))
col3.metric('Average UnitPrice', ('{}'.format(round(dataCountry['UnitPrice'].mean(), 1))))

# Dataframe
st.write("")
st.dataframe(data = dataCountry)

# Time serie chart
st.write("")
st.write(alt.Chart(dataTimeChart)
            .mark_line()
            .encode(
                x = 'InvoiceDate',
                y = 'Quantity'
            )
)

# Bar chart
st.write("")
st.write(alt.Chart(dataBarchart)
            .mark_bar()
            .encode(y = alt.Y('Country', sort = None), x = 'Quantity')
)