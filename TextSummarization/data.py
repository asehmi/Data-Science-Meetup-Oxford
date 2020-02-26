import pandas as pd
import numpy as np
import streamlit as st

import spacy

@st.cache(persist=False, allow_output_mutation=True)
def load_data(article_file, path=""):
    with open(f'{path}data/{article_file}', 'r', encoding='utf-8') as f:
        data = f.read()
    return data

@st.cache(allow_output_mutation=True)
def load_model(name):
    return spacy.load(name)
