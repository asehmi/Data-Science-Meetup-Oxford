import pandas as pd
import numpy as np
import streamlit as st
import altair as alt
import plotly.express as px

import unittest

from data import (load_data, clean_and_reshape_data)
from LayoutAndStyleUtils import (Grid, Cell, BlockContainerStyler)

import TestFixtures

def main():
    st.sidebar.header("Settings")
    
    # GET DATA
    data = load_data()
    data_unpivoted = clean_and_reshape_data(data)
    
    # >> DISPLAY WIDGETS <<

    # FILTER TO SELECTED LOCATION & YEAR
    year = st.sidebar.slider('Select year', min_value=2015, max_value=2022, value=2020)
    locations_list = list(data_unpivoted.loc[:,'Location'].sort_values(ascending=True).unique())
    location = st.sidebar.selectbox('Select location', locations_list, index=locations_list.index('United Kingdom'))
    
    data_view = data_unpivoted.loc[(data_unpivoted.loc[:,'Location'] == location) & (data_unpivoted.loc[:,'Year'] == year)]

    if st.checkbox('Show data', False):
        '''
        ### Data

        _The sample data used in this application is property of Oxford Economics and provided for personal use and_
        _educational purposes only. A 5yr rolling mean transformation has been applied to the original data series values_
        _and so is still representative of actual level values. Please do not redistribute this data without the express_
        _permission of the owner, Oxford Economics._
        '''
        # TABLE
        if st.checkbox('Show DataFrame', True):
            data_view

        if st.checkbox('Show Table'):
            st.table(data_view)

    '''
    ### Chart
    '''
    # chart data is calculated in two steps
    # step 1 (using data_unpivoted, filtered by location)
    chart_data = data_unpivoted[(data_unpivoted['Location'] == location)]

    indicators_list = list(chart_data.loc[:,'Indicator'].sort_values(ascending=True).unique())
    # this selection box is put into the reserved widget slot created above
    indicator = st.sidebar.selectbox('Select indicator', indicators_list)

    # step 2 (using chart_data, filtered by location's indicators)
    chart_data = chart_data[(chart_data['Indicator'] == indicator)]

    fig = alt.Chart(chart_data, title=f'{location} | {indicator}').mark_bar().encode(
    alt.X('Year:O', axis=alt.Axis(domain=False, tickSize=0)),
    alt.Y('Value', axis=alt.Axis(domain=False, tickSize=0, title='Value')),
        color='Value', tooltip=['Id','Year','Value']) \
        .properties(width=600).interactive()
    st.altair_chart(fig)

    # ABOUT
    st.sidebar.header('About')
    st.sidebar.info('Using Streamlit to build a Web App.\n\n' + \
        '(c) 2020. Oxford Economics Ltd. All rights reserved.')
    st.sidebar.markdown('---')

    # Display Readme.md
    if st.sidebar.checkbox('Readme', False):
        st.markdown('---')
        '''
        ### Readme
        '''
        with open('./README.md', 'r', encoding='utf-8') as f:
            readme = f.read()
            st.markdown(readme)

    # TESTS
    if st.sidebar.checkbox('Run Tests', False):
        st.markdown('---')
        st.title('Test Suite')
        '''
        ### Data Load Test
        '''
        suite = unittest.TestLoader().loadTestsFromModule(TestFixtures)
        result = unittest.TextTestRunner(verbosity=2).run(suite)
        if result.wasSuccessful():
            st.info(f'Test PASSED :-)')
            st.balloons()
        else:
            st.error(f'Test FAILED :-(')

    # Style
    st.sidebar.markdown('---')
    if st.sidebar.checkbox('Configure Style'):
        BlockContainerStyler().block_container_styler()

if __name__ == '__main__':
    BlockContainerStyler().set_default_block_container_style()

    # >> DISPLAY WIDGETS <<
    st.image('./images/logo.jpg', output_format='jpg')
    '''
    # My App Template
    Shows how to properly structure a Streamlit app. The app `loads data` from an xlsx file, `reshapes` and
    renders it as an `interactive Pandas dataframe table`, `static Streamlit table` and `Altair chart`.
    A few useful strategies are provided for `dynamically filtering data visualisations` and
    `showing/hiding page components` using Streamlit's UI widgets. Also included, is a simple
    `test fixtures class` (using Python's `unittest framework`), a neat trick to `render readme.md markdown`
    directly into the web page, and we make liberal use of Streamlit's _magic_ rendering of variables and literal values.
    '''
    main()


# === NOTES ===
#
# PANDAS
# We use .loc view a lot to index into df broadcast operation rather than using chained indexing since
# this can generate a SettingWithCopyWarning!
# See: http://pandas.pydata.org/pandas-docs/stable/user_guide/indexing.html#returning-a-view-versus-a-copy
#
# ALTAIR CHARTS
# Altair is a declarative statistical visualization library for Python, based on Vega and Vega-Lite, and the source is available on GitHub.
# https://altair-viz.github.io/index.html
# https://altair-viz.github.io/user_guide/encoding.html
#
# UNIT TEST
# https://docs.python.org/2/library/unittest.html