import os
import io
import pandas as pd
import numpy as np
import streamlit as st
import altair as alt
import json
import pickle
import settings

from data import (load_data, clean_and_reshape_data)

import unittest # https://docs.python.org/2/library/unittest.html

class Tests(unittest.TestCase):

    @classmethod
    def setUp(self):
        pass

    @classmethod
    def tearDown(self):
        pass

    def testDataLoad(self):
        '''
        ### Test Load
        '''
        data = pd.read_excel('data/GCFS Countries (GDP, Labour, Population, Incomes) SAMPLE.xlsx', 'GCFS Countries', keep_default_na = False) # na_values = ['NA']

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

        self.assertTrue(type(Id) == type(data_unpivoted['Id']))

        self.assertTrue(Id.sort_values(ascending=True).unique().all() == data_unpivoted['Id'].sort_values(ascending=True).unique().all())

        print(data_unpivoted)
        st.write(data_unpivoted)

if __name__ == '__main__':
    unittest.main()


