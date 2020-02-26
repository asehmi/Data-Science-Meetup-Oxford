import pandas as pd
import numpy as np
import streamlit as st

@st.cache(persist=True, allow_output_mutation=True)
def load_data():
    data = pd.read_excel('data/GCFS Countries (GDP, Labour, Population, Incomes) SAMPLE.xlsx', 'GCFS Countries', keep_default_na = False) # na_values = ['NA']
    return data

def clean_and_reshape_data(data):
    data = data.astype({'Location':'str', 'Indicator':'str', 'Units':'str', 'Scale':'str'})
    value_vars = list(data.filter(regex=('\\d')).columns)
    id_vars = ['Location', 'Indicator']
    Id =  data['Location Code']+'-'+data['Indicator Code']+'-'+data['Measurement']+ \
            '-'+data['Units']+'-'+data['Scale']
    data.loc[:,value_vars].fillna('0.0001', inplace = True) 
    data = data[id_vars+value_vars]
    data = pd.concat([Id, data], axis=1)
    data = data.rename(columns={0:'Id'})

    # unpivot data on all years
    data_unpivoted = pd.melt(data, id_vars=['Id']+id_vars, value_vars=value_vars, var_name='Year', value_name='Value').astype({'Year':'int16','Value':'float64'})
    
    return data_unpivoted
