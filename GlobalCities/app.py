import pandas as pd
import numpy as np
import streamlit as st
import altair as alt
import plotly.express as px
# TODO: See https://discuss.streamlit.io/t/is-it-possible-to-implement-multi-layer-tooltips-with-pydeck/13614/2
import pydeck as pdk

import settings

st.set_page_config(
    page_title='Global Cities Explorer',
    layout='wide',
    page_icon='🌍'
)

import streamlit_debug
streamlit_debug.set(flag=False, wait_for_client=False, host='localhost', port=8765)

from data import (load_data, load_geojson, clean_and_reshape_data)

st.image('./images/a12i_logo.png', output_format='png')
st.markdown('''
    # Global Cities Explorer

    Mapping global cities GDP, population, employment and household income

    * _The sample data used in this application is property of Oxford Economics and provided for personal use and educational purposes only._
    * _A 5yr rolling mean transformation has been applied to the original data series values and so is still representative of actual level values._
    * _Please do not redistribute this data without the expresspermission of the owner, Oxford Economics._
''')

st.sidebar.header("Settings")
region_type = st.sidebar.selectbox('Select region type', ['Cities', 'Countries', 'Both'])
top_n = st.sidebar.selectbox('Select group', ['All', 'Top 100', 'Top 50', 'Top 20'])

# GET DATA
gc_data = load_data(region_type)
geojson = load_geojson()

gc_data_unpivoted, merged = clean_and_reshape_data(gc_data, geojson)

# >> DISPLAY WIDGETS <<

# FILTER TO SELECTED INDICATOR & YEAR
year = st.sidebar.slider('Select year', min_value=2015, max_value=2022, value=2020) # data starts at 2000, but selection is from 2010 because of 10 yr GAGR
indicators_list = list(merged.loc[:,'Indicator'].sort_values(ascending=True).unique())
indicator = st.sidebar.selectbox('Select indicator', indicators_list)
merged_filtered_view = merged.loc[(merged.loc[:,'Indicator'] == indicator) & (gc_data_unpivoted.loc[:,'Year'] == year)]
# FILTER TO SELECTED MEASUREMENT
measurements_list = list(merged_filtered_view.loc[:,'Measurement'].sort_values(ascending=True).unique())
measurement = st.sidebar.selectbox('Select measurement', measurements_list, index=1)
merged_filtered_view = merged_filtered_view.loc[(merged_filtered_view.loc[:,'Measurement'] == measurement)]
# FILTER TO SELECTED UNITS + SCALE
units_scale_list = list(merged_filtered_view.loc[:,'Units > Scale'].sort_values(ascending=True).unique())
units_scale = st.sidebar.selectbox('Select Units > Scale', units_scale_list)
merged_filtered_view = merged_filtered_view.loc[(merged_filtered_view.loc[:,'Units > Scale'] == units_scale)]

if top_n != 'All':
    topN = int(top_n.replace('Top ', ''))
    merged_filtered_view = merged_filtered_view.nlargest(topN, columns='Value').tail(topN)

def render_map(layers):
    st.markdown('#### '+indicator+' : '+measurement+' : '+units_scale+' : '+str(year))
    try:
        st.pydeck_chart(pdk.Deck(
                map_style='mapbox://styles/mapbox/light-v9',
                initial_view_state=pdk.ViewState(
                    mapboxApiAccessToken=settings.MAPBOX_ACCESS_TOKEN,
                    longitude=0.0,
                    latitude=0.0,
                    zoom=2,
                    min_zoom=1,
                    max_zoom=5,
                    pitch=0
                ),
                layers = layers,
                tooltip = {"html": "{Location}, {Indicator}<br/>Year: {Year}, Value: {Value}<br/>{Units > Scale} in {Measurement}", "style": {"color": "white"}}
        ))
    except:
        st.warning('Can\'t display map with supplied settings')

def render_chart(data_choice):
    if data_choice == 'All Regions':
        # CHART
        c = alt.Chart(data=merged_filtered_view, title=indicator+' : '+measurement+' : '+units_scale+' : '+str(year)).mark_circle().encode(
            alt.X('longitude', axis=alt.Axis(domain=False, title='Longitude')),
            alt.Y('latitude', axis=alt.Axis(domain=False, title='Latitude')),
            size='Value', color='Value:Q', tooltip=['Location','Indicator','Measurement','Units > Scale','Year','Value']) \
            .properties(width=900, height=450).interactive()
        st.altair_chart(c)
    if data_choice == 'Selected Region':
        sel_location = st.selectbox('Select Location', list(merged.loc[:,'Location'].sort_values(ascending=True).unique()), key='chart_selectbox')
        # CHART
        chart_data = gc_data_unpivoted[(gc_data_unpivoted['Location'] == sel_location) & \
            (gc_data_unpivoted['Indicator'] == indicator) & (gc_data_unpivoted['Measurement'] == measurement)]
        # fig = px.bar(chart_data, title= sel_location+' : '+indicator+' : '+ measurement, \
        #     x='Year', y='Value', color='Units > Scale', height=400) # facet_col='Units > Scale', barmode='group' 
        # st.plotly_chart(fig)
        fig = alt.Chart(chart_data, title= sel_location+' : '+indicator+' : '+ measurement).mark_bar().encode(
            alt.X('Year:O', axis=alt.Axis(domain=False, tickSize=0)),
            alt.Y('Value', axis=alt.Axis(domain=False, tickSize=0, title=indicator+' : '+ measurement)),
            # row='Units > Scale',
            color='Units > Scale', tooltip=['Location','Indicator','Measurement','Units > Scale','Year','Value']) \
            .properties(width=900, height=450).interactive()
        st.altair_chart(fig)

def render_table(data_choice):
    if data_choice == 'All Regions':
        # TABLE
        merged_filtered_view
    if data_choice == 'Selected Region':
        sel_location = st.selectbox('Select Location', list(merged.loc[:,'Location'].sort_values(ascending=True).unique()), key='table_selectbox')
        # TABLE
        table_data = merged[(merged['Location'] == sel_location) & (merged['Indicator'] == indicator) \
            & (merged['Measurement'] == measurement)  & (gc_data_unpivoted['Year'] == year)]
        st.table(table_data.style.bar(subset='Value', color='grey', axis=0))
        # st.write('Longitude = %.4f, Latitude = %.4f' % (table_data['longitude'].iloc[0], table_data['latitude'].iloc[0]))

tab1, tab2, tab3, tab4 = st.tabs(['🌎 Map', '📊 Chart', '📋 Table', '💡 About'])

with tab1:
    c1, _, c3, _ = st.columns([1,0.5,5,3])
    with c1:
        COLOUR_RANGE = [
            [29,53,87,220],
            [69,123,157,220],
            [168,218,220,220],
            [241,250,238,220],
            [239,35,60,220],
            [217,4,41,220]
        ]

        TEXT_COLOUR = {
            'Black': [0,0,0,255],
            'Red': [189,27,33,255],
            'Green': [0,121,63,255],
            'Gold': [210,160,30,255]
        }

        radius_scale=1.0
        opacity=0.8
        text_colour = TEXT_COLOUR.get('Black')

        mapdata = merged_filtered_view[['Location', 'Indicator', 'Measurement', 'Year', 'Value', 'Units > Scale', 'longitude', 'latitude']]

        layer_choice = st.selectbox('Choose layer',['Scatterplot','Text','Scatterplot + Text'])
        if 'Scatterplot' in layer_choice:
            radius_scale = st.slider('Bubble size', min_value=0.1, max_value=3.0, step=0.1, value=1.0)
            opacity = st.slider('Bubble opacity', min_value=0.1, max_value=1.0, step=0.05, value=0.8)
        if 'Text' in layer_choice:
            text_colour = TEXT_COLOUR.get( st.selectbox('Text colour', list(TEXT_COLOUR.keys())) )
        radius_unit = 500000.0 # in metres

        max = mapdata['Value'].max(axis=0)
        min = mapdata['Value'].min(axis=0)
        # (max, min)

        mapdata['normValue'] = ((mapdata['Value'] / (max - min))*radius_unit*radius_scale)
        # mapdata['normValue']

        # calculate colour range mapping index to then assign fill colour
        mapdata['fillColorIndex'] = ( (mapdata['Value']-min) / (max-min) )*(len(COLOUR_RANGE) - 1)
        # max_c = int(mapdata['fillColorIndex'].max(axis=0))
        # min_c = int(mapdata['fillColorIndex'].min(axis=0))
        # (max_c, min_c)

        mapdata['fill_color'] = mapdata['fillColorIndex'].map(lambda x: COLOUR_RANGE[int(x)])
        # mapdata

        scatterplot_layer = pdk.Layer(
            type='ScatterplotLayer',
            id='scatterplot-layer',
            data=mapdata,
            pickable=True,
            get_position=['longitude', 'latitude'],
            get_radius='normValue',
            radius_min_pixels=2*radius_scale,
            radius_max_pixels=30*radius_scale,
            get_fill_color='fill_color',
            get_line_color=[128,128,128, 200],
            get_line_width=4000,
            stroked=True,
            filled=True,
            opacity=opacity
        )
        text_layer = pdk.Layer(
            type='TextLayer',
            id='text-layer',
            data=mapdata,
            pickable=True,
            get_position=['longitude', 'latitude'],
            get_text='Location',
            get_color=text_colour,
            billboard=False,
            get_size=18,
            get_angle=0,
            # Note that string constants in pydeck are explicitly passed as strings
            # This distinguishes them from columns in a data set
            get_text_anchor='"middle"',
            get_alignment_baseline='"center"'
        )

        if layer_choice == 'Scatterplot':
            layers = [scatterplot_layer]
        elif layer_choice == 'Text':
            layers = [text_layer]
        else:
            layers = [scatterplot_layer, text_layer]

    with c3:
        render_map(layers)

with tab2:
    c1, c2, _ = st.columns([1,5,1])
    with c1:
        data_choice = st.radio('Select view', ['All Regions', 'Selected Region'], index=0, key='chart_radio')
    with c2:
        render_chart(data_choice)

with tab3:
    c1, c2, _ = st.columns([1,5,1])
    with c1:
        data_choice = st.radio('Select view', ['All Regions', 'Selected Region'], index=0, key='table_radio')
    with c2:
        render_table(data_choice)

with tab4:
    # Display Readme.md
    with open('./README.md', 'r', encoding='utf-8') as f:
        readme = f.read()
        st.markdown(readme)

st.sidebar.markdown('---')

# ABOUT
st.sidebar.info('An example of using Streamlit to create a simple Global Cities data web app.\n\n' + \
    '(c) 2022. CloudOpti Ltd. All rights reserved.\n\n' + \
    'Contact: Arvindra Sehmi\nvin@cloudopti.com')


