import pandas as pd
import numpy as np
import streamlit as st
import altair as alt
import pydeck as pdk

from CAGR_Utils import (CAGR, CAGR_Rolling)

import unittest # https://docs.python.org/2/library/unittest.html

class Tests_PyDeckMap(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    # https://deckgl.readthedocs.io/en/latest/index.html
    def testPyDeckMap(self, longitude=-0.1252, latitude=51.5315):
        rows = st.slider('Number of data points', min_value=10000, max_value=50000, step=5000, value=10000, key=2)
        spread = st.slider('Spread', min_value=0.0, max_value=1.0, step=0.01, value=0.25, key=2)
        spread /= 10

        # randn generates a standard normal distribution array of shape (D0, D1,    . Dn) with mean=0 and sd=1
        # randn(1000, 2) generates a 1000 rows x 2 cols array of normally distributed data points
        df_map = pd.DataFrame(
            np.random.randn(rows, 2) * [spread, spread] + [longitude, latitude],
            columns=['longitude', 'latitude'])

        COLOUR_RANGE = [
            [29,53,87],
            [69,123,157],
            [168,218,220],
            [241,250,238],
            [239,35,60],
            [217,4,41]
        ]

        test_success_outcome = False
        try:
            # HexagonLayer bins its data points within each hex shape bucket
            st.pydeck_chart(pdk.Deck(
                map_style='mapbox://styles/mapbox/light-v9',
                initial_view_state=pdk.ViewState(
                    latitude=latitude,
                    longitude=longitude,
                    zoom=10,
                    pitch=55
                ),
                layers=[
                    pdk.Layer(
                        type='HexagonLayer',
                        data=df_map,
                        color_range=COLOUR_RANGE,
                        get_position=['longitude', 'latitude'],
                        radius=200,
                        elevation_scale=4,
                        elevation_range=[0, 1000],
                        pickable=True,
                        extruded=True,
                        opacity=0.8,
                        stroked=False,
                        filled=True
                    ),
                    pdk.Layer(
                        type='ScatterplotLayer',
                        data=df_map,
                        get_position=['longitude', 'latitude'],
                        get_color=[0,121,63, 160],
                        get_radius=200
                    ),
                ],
            ))
            test_success_outcome = True
        except:
            st.warning('Can\'t display map with supplied settings')

        st.write('First Longitude = %.4f, First Latitude = %.4f' % (df_map['longitude'].iloc[0], df_map['latitude'].iloc[0]))

        self.assertTrue(test_success_outcome == True)

# DEPRECATED
class Tests_DeckGlMap(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    # https://deck.gl/#/documentation/deckgl-api-reference/layers/overview
    def testDeckGlMap(self, longitude=-0.1252, latitude=51.5315):
        rows = st.slider('Number of data points', min_value=10000, max_value=50000, step=5000, value=10000, key=1)
        spread = st.slider('Spread', min_value=0.0, max_value=1.0, step=0.01, value=0.25, key=1)
        spread /= 10

        # randn generates a standard normal distribution array of shape (D0, D1,    . Dn) with mean=0 and sd=1
        # randn(1000, 2) generates a 1000 rows x 2 cols array of normally distributed data points
        df_map = pd.DataFrame(
            np.random.randn(rows, 2) * [spread, spread] + [longitude, latitude],
            columns=['longitude', 'latitude'])
        
        COLOUR_RANGE = [
            [29,53,87],
            [69,123,157],
            [168,218,220],
            [241,250,238],
            [239,35,60],
            [217,4,41]
        ]

        test_success_outcome = False
        try:
            # HexagonLayer bins its data points within each hex shape bucket
            st.deck_gl_chart(
                viewport={
                    'longitude': longitude,
                    'latitude': latitude,
                    'zoom': 10,
                    'pitch': 55,
                },
                layers=[{
                    'id': 'heatmap',
                    'type': 'HexagonLayer',
                    'colorRange': COLOUR_RANGE,
                    'data': df_map,
                    'getLongitude': 'longitude',
                    'getLatitude': 'latitude',
                    'radius': 200,
                    'coverage': 1,
                    'upperPercentile': 100,
                    'elevationScale': 4,
                    'elevationRange': [0, 1000],
                    'pickable': True,
                    'extruded': True,
                    'opacity': 0.8,
                    'stroked': False,
                    'filled': True
                }, {
                    'type': 'ScatterplotLayer',
                    'data': df_map,
                    'getColor': [209,162,30, 160],
                    'get_radius':200
                }]
            )
            test_success_outcome = True
        except:
            st.warning('Can\'t display map with supplied settings')

        st.write('First Longitude = %.4f, First Latitude = %.4f' % (df_map['longitude'].iloc[0], df_map['latitude'].iloc[0]))

        self.assertTrue(test_success_outcome == True)

class Tests_CAGR(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testSimpleCAGR(self):
        st.markdown('### Simple CAGR calculation over period 2000-2015')

        df = pd.DataFrame({
            'Id':['A','B','C','D'],
            '2000':[7,6,5,4],
            '2001':[1,9,9,8],
            '2002':[2,0,0,1],
            '2003':[3,5,6,8],
            '2004':[5,6,7,5],
            '2005':[1,3,4,5],
            '2006':[2,3,6,7],
            '2007':[8,3,5,0],
            '2008':[1,3,5,7],
            '2009':[2,4,6,8],
            '2010':[3,6,9,1],
            '2011':[9,6,3,1],
            '2012':[5,5,5,5],
            '2013':[4,7,3,2],
            '2014':[0,4,6,9],
            '2015':[8,3,7,1]
        }).set_index('Id')

        CAGR_call_pattern_1 = df.apply(
            func=CAGR,    
            axis=1, 
            # positional arguments (i.e. order matters)
            args=(df.columns[-1],df.columns[0], len(df.columns)-1)
        )

        CAGR_call_pattern_2 = df.apply(
            func=CAGR,
            axis=1,
            args=('2015','2000', len(df.columns)-1)
        )

        assert(CAGR_call_pattern_1.equals(CAGR_call_pattern_2))

        st.write('num_periods: {}'.format(len(df.columns)-1))

        df['CAGR_call_pattern_1'] = CAGR_call_pattern_1
        df['CAGR_call_pattern_2'] = CAGR_call_pattern_2

        print(df)
        st.dataframe(df)

        self.assertTrue(df['CAGR_call_pattern_1'].all() == df['CAGR_call_pattern_2'].all())


    def testRollingCAGR(self):
        st.markdown('### Rolling 5 year CAGR calculation over period 2000-2015')

        df = pd.DataFrame({
            'Id':['A','B','C','D'],
            '2000':[7,6,5,4],
            '2001':[1,9,9,8],
            '2002':[2,0,0,1],
            '2003':[3,5,6,8],
            '2004':[5,6,7,5],
            '2005':[1,3,4,5],
            '2006':[2,3,6,7],
            '2007':[8,3,5,0],
            '2008':[1,3,5,7],
            '2009':[2,4,6,8],
            '2010':[3,6,9,1],
            '2011':[9,6,3,1],
            '2012':[5,5,5,5],
            '2013':[4,7,3,2],
            '2014':[0,4,6,9],
            '2015':[8,3,7,1]
        }).set_index('Id')

        value_vars = list(df.filter(regex=('\\d')).columns)
        # value_vars

        df = pd.DataFrame(df).reset_index()

        # unpivot df on all years
        df_unpivoted = pd.melt(df, id_vars=['Id'], value_vars=value_vars, var_name='Year', value_name='Value').astype({'Year':'int16','Value':'float64'})
        df_cagr = CAGR_Rolling(df_unpivoted, 5, 'CAGR (5Y)', ['Id'], 'Year', 'Value')
        
        print('num_periods: 5')
        print(df_cagr)
        st.write('num_periods: 5')
        st.dataframe(df_cagr)

class Tests_AVG(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testRollingAVG(self):
        st.markdown('### Rolling AVG calculation')

        df = pd.DataFrame(np.random.randn(365, 1),
                          index=range(365),
                          columns=['A'])

        num_periods = st.slider('Num periods', 1, 90, 7, 1)
        df[f'A({num_periods})'] = df.rolling(window=num_periods, center=True).A.mean()

        df = df[['A', f'A({num_periods})']]
        
        st.markdown(f'### num_periods: {num_periods}')
        st.dataframe(df)

        st.markdown(f'### {num_periods}-day rolling average')
        df.plot(subplots=True)
        st.pyplot()

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(Tests_PyDeckMap)
    unittest.TextTestRunner(verbosity=2).run(suite)
    unittest.main()
