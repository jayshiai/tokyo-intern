# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
#%%
df_1 = pd.read_csv('selected_df_high accuracy.csv')
df_2 = pd.read_csv('selected_df_low accuracy.csv')
#%%
print(df_1[['weight','sents','hojin_id']])
print(df_2[['weight','sents','hojin_id']])
print(df_1[df_1['hightechflag']==1])
print(df_2[df_2['hightechflag']==1])
#%%
import nltk
from nltk.corpus import stopwords
from gensim import corpora, models
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer
import string
from gensim.models.ldamodel import LdaModel
from sklearn.cluster import KMeans
from sklearn import metrics
from scipy.spatial.distance import cdist
import numpy as np
import matplotlib.pyplot as plt
from gensim.models import CoherenceModel
#%%
def pre_process(df,hojin):
    lst = df[df['hojin_id']==hojin]['sents'].tolist()
    word_total = []
    for sent in lst:
        word_sent = sent.split('|')
        for word in word_sent:
            word_total.append(word)
    return word_total
def Vectorization(word_dictionary):
    texts = [word_dictionary[i] for i in word_dictionary.keys()]
    dictionary = corpora.Dictionary(texts)
    corpus = [dictionary.doc2bow(text) for text in texts]
    tfidf = models.TfidfModel(corpus)
    corpus_tfidf = tfidf[corpus]
    vector_bow = {idb:[(dictionary[ids],count) for ids,count in doc] for idb,doc in enumerate(corpus)}
    vector_tfidf = {idt:[(dictionary[ids],np.around(tf,decimals=2)) for ids,tf in doc] for idt,doc in enumerate(corpus_tfidf)}
    return (vector_bow,vector_tfidf,corpus,dictionary,texts)
def keyword(vector,n):
    vector_sorted = {}
    vector_keywords = {}
    for i in vector.keys():
        lst1 = []
        lst1.append(vector[i])
        sorted_lst = sorted(lst1[0],key=lambda x:x[1],reverse=True)
        keyword_lst = [word for word,value in sorted_lst[:n]]
        vector_sorted[i] = sorted_lst
        vector_keywords[i] = keyword_lst
    return (vector_sorted,vector_keywords)
#%% For Dataframe 1
hojinid_1 = list(set(df_1['hojin_id'].tolist()))
dct_1 = {}
for ids in hojinid_1:
    words = pre_process(df_1,ids)
    dct_1[f'{ids}'] = words

bow_vector_1 = Vectorization(dct_1)[0]
tfidf_vector_1 = Vectorization(dct_1)[1]
bow_corpus_1 = Vectorization(dct_1)[2]
gensim_dict_1 = Vectorization(dct_1)[3]
bow_keyword_1 = keyword(bow_vector_1,5)[1]
tfidf_keyword_1 = keyword(tfidf_vector_1,5)[1]
text_1 = Vectorization(dct_1)[4]
lda_1 = LdaModel(bow_corpus_1, num_topics=40, id2word=gensim_dict_1, passes=15)
#%% Check dictionary
print(dct_1[str(hojinid_1[2])])
#%% Check topics
topics_1 = lda_1.print_topics(num_words=10)
for topic in topics_1:
    print(topic)
#doc_topics_1 = lda_1.get_document_topics(bow_corpus_1[203])
#print(doc_topics_1)
#%%
hojinid_2 = list(set(df_2['hojin_id'].tolist()))
dct_2 = {}
for ids in hojinid_2:
    words = pre_process(df_2,ids)
    dct_2[f'{ids}'] = words

bow_vector_2 = Vectorization(dct_2)[0]
tfidf_vector_2 = Vectorization(dct_2)[1]
bow_corpus_2 = Vectorization(dct_2)[2]
gensim_dict_2 = Vectorization(dct_2)[3]
bow_keyword_2 = keyword(bow_vector_2,5)[1]
tfidf_keyword_2 = keyword(tfidf_vector_2,5)[1]
text_2 = Vectorization(dct_2)[4]
lda_2 = LdaModel(bow_corpus_2, num_topics=40, id2word=gensim_dict_2, passes=15)

#%% Check dictionary
print(dct_2[str(hojinid_2[2])])
#%% Check topics
topics_2 = lda_2.print_topics(num_words=10)
for topic in topics_2:
    print(topic)
#doc_topics_1 = lda_1.get_document_topics(bow_corpus_1[203])
#print(doc_topics_1)

#%%
# Compute Coherence Score
coherence_model_lda_1 = CoherenceModel(model=lda_1, texts=text_1, dictionary=gensim_dict_1, coherence='c_v')
coherence_lda_1 = coherence_model_lda_1.get_coherence()
print('Coherence Score model 1: ', coherence_lda_1)
coherence_model_lda_2 = CoherenceModel(model=lda_2, texts=text_2, dictionary=gensim_dict_2, coherence='c_v')
coherence_lda_2 = coherence_model_lda_2.get_coherence()
print('Coherence Score model 2: ', coherence_lda_2)
#%%
