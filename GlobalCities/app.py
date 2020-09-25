import pandas as pd
import numpy as np
import streamlit as st
import altair as alt
import plotly.express as px
import pydeck as pdk

import settings

from data import (load_data, load_geojson, clean_and_reshape_data)
from LayoutAndStyleUtils import (Grid, Cell, BlockContainerStyler)
from TestFixtures import (Tests_DeckGlMap, Tests_PyDeckMap, Tests_CAGR, Tests_AVG)

import unittest

BlockContainerStyler().set_default_block_container_style()

st.image('./images/logo.jpg', output_format='jpg')
'''
# Global cities explorer

Mapping global cities GDP, population, employment and household income

_The sample data used in this application is property of Oxford Economics and provided for personal use and_
_educational purposes only. A 5yr rolling mean transformation has been applied to the original data series values_
_and so is still representative of actual level values. Please do not redistribute this data without the express_
_permission of the owner, Oxford Economics._
'''

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

'''
### Map
'''
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

st.sidebar.header("Map settings")
mapdata = merged_filtered_view[['Location', 'Indicator', 'Measurement', 'Year', 'Value', 'Units > Scale', 'longitude', 'latitude']]

layer_choice = st.sidebar.selectbox('Choose layer',['Scatterplot','Text','Scatterplot + Text'])
if 'Scatterplot' in layer_choice:
    radius_scale = st.sidebar.slider('Bubble size', min_value=0.1, max_value=3.0, step=0.1, value=1.0)
    opacity = st.sidebar.slider('Bubble opacity', min_value=0.1, max_value=1.0, step=0.05, value=0.8)
if 'Text' in layer_choice:
    text_colour = TEXT_COLOUR.get( st.sidebar.selectbox('Text colour', list(TEXT_COLOUR.keys())) )
radius_unit = 500000.0 # in metres

max = mapdata.loc[:,'Value'].max(axis=0)
min = mapdata.loc[:,'Value'].min(axis=0)
# (max, min)

mapdata.loc[:,'normValue'] = ((mapdata.loc[:,'Value'] / (max - min))*radius_unit*radius_scale)

# calculate colour range mapping index to then assign fill colour
mapdata.loc[:,'fillColorIndex'] = ( (mapdata.loc[:,'Value']-min) / (max-min) )*(len(COLOUR_RANGE) - 1)
# max_c = mapdata.loc[:,'fillColorIndex'].max(axis=0)
# min_c = mapdata.loc[:,'fillColorIndex'].min(axis=0)
# (max_c, min_c)
mapdata.loc[:,'fill_color'] = mapdata.loc[:,'fillColorIndex'].map(lambda x: COLOUR_RANGE[int(x)])

# st.write(mapdata.dtypes)
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
    get_text_anchor='middle',
    get_alignment_baseline='center'
)

if layer_choice == 'Scatterplot':
    layers = [scatterplot_layer]
elif layer_choice == 'Text':
    layers = [text_layer]
else:
    layers = [scatterplot_layer, text_layer]

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

'''
### Data Table and Chart
'''
data_choice = st.radio('Select view', ['None','All Regions', 'Selected Region'], index=1)
if data_choice == 'All Regions':
    # CHART
    c = alt.Chart(data=merged_filtered_view, title=indicator+' : '+measurement+' : '+units_scale+' : '+str(year)).mark_circle().encode(
        alt.X('longitude', axis=alt.Axis(domain=False, title='Longitude')),
        alt.Y('latitude', axis=alt.Axis(domain=False, title='Latitude')),
        size='Value', color='Value:Q', tooltip=['Location','Indicator','Measurement','Units > Scale','Year','Value']) \
        .properties(width=900, height=450).interactive()
    st.altair_chart(c)
    # TABLE
    merged_filtered_view
if data_choice == 'Selected Region':
    sel_location = st.selectbox('Select Location', list(merged.loc[:,'Location'].sort_values(ascending=True).unique()))
    # CHART
    chart_data = gc_data_unpivoted.loc[(gc_data_unpivoted.loc[:,'Location'] == sel_location) & \
        (gc_data_unpivoted.loc[:,'Indicator'] == indicator) & (gc_data_unpivoted.loc[:,'Measurement'] == measurement)]
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
    # TABLE
    table_data = merged.loc[(merged.loc[:,'Location'] == sel_location) & (merged.loc[:,'Indicator'] == indicator) \
        & (merged.loc[:,'Measurement'] == measurement)  & (gc_data_unpivoted.loc[:,'Year'] == year)]
    st.table(table_data.style.bar(subset='Value', color='grey', axis=0))
    # st.write('Longitude = %.4f, Latitude = %.4f' % (table_data['longitude'].iloc[0], table_data['latitude'].iloc[0]))

# ABOUT
st.sidebar.header('About')
st.sidebar.info('An example of using Streamlit to create a simple Global Cities data web app.\n\n' + \
    '(c) 2020. Oxford Economics Ltd. All rights reserved.\n\n' + \
    'Contact: Arvindra Sehmi\nasehmi@oxfordeconomics.com')

# Display Readme.md
if st.sidebar.checkbox('Readme', False):
    st.markdown('---')
    '''
    ### Readme
    '''
    with open('./README.md', 'r', encoding='utf-8') as f:
        readme = f.read()
        st.markdown(readme)

st.sidebar.markdown('---')

# TESTS
result = None

st.markdown('---')
if st.sidebar.checkbox('Deck GL test'):
    st.title('Deck.GL test')
    suite = unittest.TestLoader().loadTestsFromTestCase(Tests_DeckGlMap)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    if result != None and result.wasSuccessful():
        st.info(f'Test PASSED :-)')
        # st.balloons()
    elif result != None:
        st.error(f'Test FAILED :-(')

if st.sidebar.checkbox('PyDeck test'):
    st.title('PyDeck test')
    suite = unittest.TestLoader().loadTestsFromTestCase(Tests_PyDeckMap)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    if result != None and result.wasSuccessful():
        st.info(f'Test PASSED :-)')
        # st.balloons()
    elif result != None:
        st.error(f'Test FAILED :-(')

if st.sidebar.checkbox('CAGR tests'):
    st.title('CAGR test')
    suite = unittest.TestLoader().loadTestsFromTestCase(Tests_CAGR)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    if result != None and result.wasSuccessful():
        st.info(f'Test PASSED :-)')
        # st.balloons()
    elif result != None:
        st.error(f'Test FAILED :-(')

if st.sidebar.checkbox('AVG tests'):
    st.title('AVG test')
    suite = unittest.TestLoader().loadTestsFromTestCase(Tests_AVG)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    if result != None and result.wasSuccessful():
        st.info(f'Test PASSED :-)')
        # st.balloons()
    elif result != None:
        st.error(f'Test FAILED :-(')

# Style
st.sidebar.markdown('---')
if st.sidebar.checkbox('Configure Style'):
    BlockContainerStyler().block_container_styler()
    

# === NOTES ===
#
# PANDAS
# We use .loc view a lot to index into df broadcast operation rather than using chained indexing since
# this can generate a SettingWithCopyWarning!
# See: # http://pandas.pydata.org/pandas-docs/stable/user_guide/indexing.html#returning-a-view-versus-a-copy
# 
# SQL queries in Pandas: https://pandas.pydata.org/pandas-docs/stable/getting_started/comparison/comparison_with_sql.html
#
# ALTAIR CHARTS
# Altair is a declarative statistical visualization library for Python, based on Vega and Vega-Lite, and the source is available on GitHub.
# https://altair-viz.github.io/index.html
# https://altair-viz.github.io/user_guide/encoding.html
#
# DECK.GL MAPS
# WebGL-powered framework for visual exploratory data analysis of large datasets.
# https://deck.gl/
# https://deck.gl/#/examples/overview
# https://deck.gl/#/documentation/developer-guide/using-layers
# https://deck.gl/#/documentation/deckgl-api-reference/layers/overview
# https://deck.gl/#/documentation/deckgl-api-reference/layers/scatterplot-layer
# https://deck.gl/#/documentation/deckgl-api-reference/layers/hexagon-layer
#
# PYDECK.GL MAPS
# https://deckgl.readthedocs.io/en/latest/index.html
#

### OLD DECK.GL MAP CODE ##################################

    # mapdata.loc[:,'colorR'] = mapdata.loc[:,'fillColorIndex'].map(lambda x: COLOUR_RANGE[int(x)][0])
    # mapdata.loc[:,'colorG'] = mapdata.loc[:,'fillColorIndex'].map(lambda x: COLOUR_RANGE[int(x)][1])
    # mapdata.loc[:,'colorB'] = mapdata.loc[:,'fillColorIndex'].map(lambda x: COLOUR_RANGE[int(x)][2])

    # scatterplot_layer = {
    #     'type': 'ScatterplotLayer',
    #     'id': 'scatterplot-layer',
    #     'data': mapdata,
    #     'pickable': True,
    #     'getLongitude': 'longitude',
    #     'getLatitude': 'latitude',
    #     'getRadius': 'normValue',
    #     'radiusScale': 1,
    #     'radiusMaxPixels': 30*radius_scale,
    #     'radiusMinPixels': 3*radius_scale,
    #     'getLineColor': [128,128,128, 200],
    #     'getLineWidth': 4000,
    #     'stroked': True,
    #     'filled': True,
    #     'opacity': opacity
    # }
    # text_layer = {
    #     'type' : 'TextLayer',
    #     'id': 'text-layer',
    #     'data': mapdata,
    #     'pickable': True,
    #     'getLongitude': 'longitude',
    #     'getLatitude': 'latitude',
    #     'getText': 'Location',
    #     'getColor': [210,160,30,255],
    #     'billboard': False,
    #     'getSize': 18,
    #     'getAngle': 0,
    #     'getTextAnchor': 'middle',
    #     'getAlignmentBaseline': 'center'
    # }

    # if layer_choice == 'Scatterplot':
    #     layers = [scatterplot_layer]
    # elif layer_choice == 'Text':
    #     layers = [text_layer]
    # else:
    #     layers = [scatterplot_layer, text_layer]

    # st.markdown('#### '+indicator+' : '+measurement+' : '+units_scale+' : '+str(year))

    # try:
    #     st.pydeck_chart(pdk.Deck(
    #             map_style='mapbox://styles/mapbox/light-v9',
    #             initial_view_state=pdk.ViewState(
    #                 # mapboxApiAccessToken=settings.MAPBOX_ACCESS_TOKEN,
    #                 longitude=0.0,
    #                 latitude=0.0,
    #                 zoom=2,
    #                 min_zoom=1,
    #                 max_zoom=5,
    #                 pitch=0
    #             ),
    #             layers = layers
    #     ))
    #     st.deck_gl_chart(
    #         viewport = {
    #             'mapStyle': 'mapbox://styles/mapbox/light-v10',
    #             'mapboxApiAccessToken': settings.MAPBOX_ACCESS_TOKEN,
    #             'longitude': 0.0,
    #             'latitude': 0.0,
    #             'zoom': 2,
    #             'minZoom': 1,
    #             'maxZoom': 5,
    #             'pitch': 0
    #         },
    #         layers = layers
    #     )
    # except:
    #     st.warning('Can\'t display map with supplied settings')

###########################################################

