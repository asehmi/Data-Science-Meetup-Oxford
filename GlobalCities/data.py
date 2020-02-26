import pandas as pd
import numpy as np
import streamlit as st

from CAGR_Utils import CAGR_Rolling

@st.cache(persist=True)
def load_data(region_type):
    if region_type == 'Countries':
        gc_data = load_data_countries()
    elif region_type == 'Cities':
        gc_data = load_data_cities()
    else:
        gc_countries = load_data_countries()
        gc_cities = load_data_cities()
        gc_data = pd.concat([gc_countries, gc_cities],ignore_index=True,axis=0,sort=False)
        gc_data.reset_index()

    return gc_data

@st.cache(persist=True)
def load_data_countries():
    gc_data_countries = pd.read_excel('GCFS Countries (GDP, Labour, Population, Incomes) SAMPLE.xlsx', keep_default_na=False, na_values=["NA"])
    return gc_data_countries

@st.cache(persist=True)
def load_data_cities():
    gc_data_cities = pd.read_excel('GCFS Cities (GDP, Labour, Population, Incomes) SAMPLE.xlsx', keep_default_na = False, na_values = ['NA'])
    return gc_data_cities

@st.cache(persist=True)
def load_geojson():
    geojson = pd.read_json('gcfs-geojson.json', orient='records')
    geojson = pd.read_json(geojson['properties'].to_json(orient='records'),orient='records')
    geojson = geojson[['locationCode','latitude','longitude']]
    return geojson

@st.cache(persist=True)
def clean_and_reshape_data(gc_data, geojson):

    # UNPIVOT DATA
    value_vars = list(gc_data.filter(regex=('\\d')).columns)
    # value_vars
    # unpivot the dataframe on all years 
    gc_data_unpivoted = pd.melt(gc_data, id_vars=['Location','Indicator','Measurement','Units','Scale', 'Location Code'], \
         value_vars=value_vars, var_name='Year', value_name='Value').astype({'Year':'int16','Value':'float64'})
    gc_data_unpivoted = gc_data_unpivoted.sort_values(['Location','Indicator','Measurement','Units','Scale','Year'])
    gc_data_unpivoted.loc[:,'Value'].fillna(method='bfill', inplace = True)
    # st.dataframe(gc_data_unpivoted.head(100))

    # GENERATE ROLLING CAGR SERIES AND APPEND
    gc_data_cagr_3y = CAGR_Rolling(gc_data_unpivoted, num_periods=3, cagr_col='CAGR (3Y)', \
        id_vars=['Location', 'Indicator', 'Measurement', 'Units', 'Scale', 'Location Code'], \
        value_var_col='Year', value_col='Value')
    gc_data_cagr_3y = gc_data_cagr_3y.drop(['Value'], axis=1)
    gc_data_cagr_3y = gc_data_cagr_3y.rename(columns={'CAGR (3Y)': 'Value'})
    gc_data_cagr_3y.loc[:,'Measurement'] = 'CAGR (3Y)'
    gc_data_cagr_3y.loc[:,'Units'] = '%'
    # st.dataframe(gc_data_cagr_3y.head(100))

    # append data frames (they both have identical columns)
    gc_data_unpivoted = pd.concat([gc_data_unpivoted, gc_data_cagr_3y],ignore_index=True,axis=0,sort=False)
    gc_data_unpivoted.reset_index()

    gc_data_unpivoted.loc[:,'Units > Scale'] = \
        [(gc_data_unpivoted.loc[i,'Units'] + (', ' + gc_data_unpivoted.loc[i,'Scale']) \
        if len(gc_data_unpivoted.loc[i,'Scale']) != 0 \
        else gc_data_unpivoted.loc[i,'Units']) \
        for i in gc_data_unpivoted.index ]

    # JOIN UNPIVOTED DATA WITH GEOJSON
    # merge filtered data with geojson to get lat/lon columns; throw away [locationCode] from geojson
    merged = pd.merge(gc_data_unpivoted, geojson, how='left', left_on='Location Code', right_on='locationCode') \
                [['Location', 'Indicator', 'Measurement', 'Units', 'Scale', 'Year', 'Value', 'Location Code', 'Units > Scale', 'longitude', 'latitude']]
    # st.dataframe(merged.head(100))
    # st.dataframe(merged.tail(100))

    return gc_data_unpivoted, merged
