import pandas as pd
import numpy as np
import streamlit as st

from gensim.summarization import summarize # Requires: python -c "import nltk; nltk.download('punkt')"

from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lex_rank import LexRankSummarizer

import unittest

from data import load_data
from TF_IDF import tf_idf

def main():
    st.sidebar.header("Settings")

    article = st.sidebar.selectbox('Select article', ['Health Data', 'Coronavirus', 'Huawei'])
    if article == 'Health Data':
        article_file = 'text_sample_1.txt'
    elif article == 'Coronavirus':
        article_file = 'text_sample_2.txt'
    else:
        article_file = 'text_sample_3.txt'
    
    # GET DATA
    text = load_data(article_file)
    
    # TABLE
    st.sidebar.subheader('Data view')
    if st.sidebar.checkbox('Show Full Text', False):
        '''
        ### Data
        '''
        text

    # TABLE
    st.sidebar.subheader('Summary view')
    if st.sidebar.checkbox('Gensim Summary', True):
        '''
        ### Gensim Summary
        '''
        sentences_ratio = st.sidebar.slider('Ratio of sentences in summary', 0.05, 1.0, 0.25, 0.05)
        gensim_summary_list = summarize(text, ratio=sentences_ratio, split=True)
        gensim_summary = ' '.join(gensim_summary_list)
        gensim_summary

    if st.sidebar.checkbox('Sumy Summary', True):
        '''
        ### Sumy Summary
        '''
        num_sentences = st.sidebar.slider('Number of sentences in summary', 1, 15, 9, 1)
        # https://www.aaai.org/Papers/JAIR/Vol22/JAIR-2214.pdf
        parser = PlaintextParser.from_string(text,Tokenizer("english"))
        lex_summarizer = LexRankSummarizer()
        sumy_lex_rank = lex_summarizer(parser.document,num_sentences)
        sumy_summary_list = [str(sentence) for sentence in sumy_lex_rank]
        sumy_summary = ' '.join(sumy_summary_list)
        sumy_summary

    if st.sidebar.checkbox('Tf-Idf Summary', True):
        '''
        ### Tf-Idf Summary
        '''
        threshold = st.sidebar.slider('Tf-Idf threshold factor', 0.0, 1.0, 0.75, 0.01)
        tf_idf_summary = tf_idf().summarize(text, threshold)
        tf_idf_summary
   
    # ABOUT
    st.sidebar.header('About')
    st.sidebar.info('**Text Summarization App**\n' + \
        'Examples using `Gensim`, `Sumy` and `NLTK + custom Tf-Idf` implementations.\n\n' + \
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

if __name__ == '__main__':
    # >> DISPLAY WIDGETS <<
    st.image('./images/logo.jpg', output_format='jpg')
    '''
    # Text Summarization App
    '''
    main()


# === NOTES ===
#
# UNIT TEST
# https://docs.python.org/2/library/unittest.html