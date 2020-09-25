import os
import io
import pandas as pd
import numpy as np
import streamlit as st
import altair as alt
import json
import pickle
import settings
import time
import math
import random

from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lex_rank import LexRankSummarizer

from data import load_data
from TF_IDF import tf_idf

import unittest # https://docs.python.org/2/library/unittest.html

class Test_TF_IDF(unittest.TestCase):

    def testTfIdf(self):
        text = load_data('text_sample_1.txt')
        summary = tf_idf().summarize(text, 0.8)
        print(summary)

class Test_Sumy(unittest.TestCase):

    def testSumy(self):
        text = load_data('text_sample_1.txt')
        parser = PlaintextParser.from_string(text,Tokenizer("english"))
        lex_summarizer = LexRankSummarizer()
        sumy_lex = lex_summarizer(parser.document,5)
        sumy_summary_list = [str(sentence) for sentence in sumy_lex]
        sumy_summary = ' '.join(sumy_summary_list)
        print(sumy_summary)

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(Test_TF_IDF)
    unittest.TextTestRunner(verbosity=2).run(suite)
    #unittest.main()
