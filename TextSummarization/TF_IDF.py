import math
import pandas as pd

import spacy # Requires: python -m spacy download en_core_web_sm
from spacy import displacy

from nltk import sent_tokenize, word_tokenize, PorterStemmer
from nltk.corpus import stopwords

from data import load_model

import streamlit as st

class tf_idf():

    nlp = load_model('en_core_web_md')

    def word_freq(self, text) -> dict:
        """
        Create document word frequency table {w1:f1, ..., wN:fN}.
        Remove stop words, punct, etc. and lowercase
        :rtype: dict
        """
        doc = self.nlp(text)
        word_freq_table = {}
        for token in doc:
            ignore = token.is_stop or token.is_punct or token.is_quote or token.is_oov or token.text in ['.',',',';',':','%','-']
            if not ignore and token.text in word_freq_table:
                word_freq_table[token.lower_] += 1
            elif not ignore:
                word_freq_table[token.lower_] = 1

        return word_freq_table

    def sent_word_freq(self, text) -> dict:
        """
        Create sentence word frequency table {s1:{w1:f1, ..., wN:fN}, ..., sN:{w1:f1, ..., wN:fN} }.
        :rtype: dict
        """
        doc = self.nlp(text)
        sent_word_freq_table = {}
        for sent in doc.sents:
            word_freq_table = self.word_freq(sent.lower_)
            sent_word_freq_table[sent.lower_[:15]] = word_freq_table

        return sent_word_freq_table

    def tf_matrix(self, sent_word_freq_table) -> dict:
        tf_matrix = {}
        for sent, word_freq_table in sent_word_freq_table.items():
            tf_table = {}
            sent_word_count = len(word_freq_table)
            for word, freq in word_freq_table.items():
                tf_table[word] = freq / sent_word_count
            tf_matrix[sent] = tf_table

        return tf_matrix

    def global_word_freq(self, tf_matrix) -> dict:
        tf_global_matrix = {}
        for sent, f_table in tf_matrix.items():
            for word, count in f_table.items():
                if word in tf_global_matrix:
                    tf_global_matrix[word] += count
                else:
                    tf_global_matrix[word] = count

        return tf_global_matrix


    def idf(self, tf_matrix, tf_global_matrix) -> dict:
        total_documents = len(tf_matrix)
        idf_matrix = {}
        for sent, f_table in tf_matrix.items():
            idf_table = {}
            for word in f_table.keys():
                idf_table[word] = math.log10(total_documents / float(tf_global_matrix[word]))
            idf_matrix[sent] = idf_table

        return idf_matrix


    def tf_idf(self, tf_matrix, idf_matrix) -> dict:
        tf_idf_matrix = {}
        for (sent1, f_table1), (sent2, f_table2) in zip(tf_matrix.items(), idf_matrix.items()):
            tf_idf_table = {}
            for (word1, value1), (word2, value2) in zip(f_table1.items(),f_table2.items()):  # here, keys are the same in both the table
                tf_idf_table[word1] = float(value1 * value2)
            tf_idf_matrix[sent1] = tf_idf_table

        return tf_idf_matrix

    def score_sentences(self, tf_idf_matrix) -> dict:
        # Score sentences by their word TFs
        # Algorithm: adds word TFs and divides by total no of words in sentence. Normalise scale in range [0..10]
        sentenceScores = {}
        for sent, f_table in tf_idf_matrix.items():
            sent_word_count = len(f_table)
            scores = [score for _word, score in f_table.items()]
            if len(scores) > 0:
                maxScore = max(scores)
                normScores = [score/maxScore for score in scores]
                total_sent_score = sum(normScores)
                sentenceScores[sent] = total_sent_score / sent_word_count
            else:
                sentenceScores[sent] = 0.0

        return sentenceScores

    def average_score(self, sentenceScores) -> int:
        sumScores = sum([sentenceScores[entry] for entry in sentenceScores])
        # Average score of a sentence from original summary_text
        average = sumScores / len(sentenceScores)

        return average


    def generate_summary(self, sents, sentenceScores, threshold) -> str:
        summary = ' '.join([
            sent.text.strip() for sent in sents
            if ((sent.lower_[:15] in sentenceScores) and (sentenceScores[sent.lower_[:15]] <= (threshold)))
        ])
        return summary

    def summarize(self, text, threshold: float) -> str:
        doc = self.nlp(text)
        sents = doc.sents
    
        '''
        Term frequency (TF) is how often a word appears in the document, divided by how many words there are in the document.
        '''
        # 1 Calculate the term frequency matrix, by sentence
        tf_matrix = self.sent_word_freq(text)
        #st.write(pd.DataFrame(tf_matrix))

        # 2 Calculate the term frequency matrix, global (all sentences)
        tf_global_matrix = self.global_word_freq(tf_matrix)
        #st.write(pd.DataFrame({'tf_global_matrix':tf_global_matrix}))

        '''
        Inverse document frequency (IDF) is how unique or rare a word is.
        '''
        # 3 Calculate IDF
        idf_matrix = self.idf(tf_matrix, tf_global_matrix)
        #st.write(pd.DataFrame(idf_matrix))

        # 4 Calculate TF-IDF
        tf_idf_matrix = self.tf_idf(tf_matrix, idf_matrix)
        #st.write(pd.DataFrame(tf_idf_matrix))

        # 5 Score sentences
        sentence_scores = self.score_sentences(tf_idf_matrix)
        #st.write(pd.DataFrame({'sentence_scores':sentence_scores}))

        # 6 Generate summary
        summary = self.generate_summary(sents, sentence_scores, threshold)

        return summary
