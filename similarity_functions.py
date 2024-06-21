import json
import requests
import html5lib
import bs4
from bs4 import BeautifulSoup
import nltk, string
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.tokenize import word_tokenize, sent_tokenize
import scipy
import gensim
import gensim.downloader as api
import transformers
import numpy
from typing import Callable

def sim_func1(query, corpus_of_documents):
    query = query.lower().split(" ")
    sims = []
    for document in corpus_of_documents:
        document = document.lower().split(" ")
        intersection = set(query).intersection(set(document))
        union = set(query).union(set(document))
        sims.append(len(intersection)/len(union))
    return sims

def sim_func2(query, corpus_of_documents):
    gen_docs = [[w.lower() for w in word_tokenize(text)]
        for text in corpus_of_documents]
    dictionary = gensim.corpora.Dictionary(gen_docs)
    corpus = [dictionary.doc2bow(gen_doc) for gen_doc in gen_docs]
    tf_idf = gensim.models.TfidfModel(corpus)
    sims = gensim.similarities.Similarity('workdir/',tf_idf[corpus], num_features=len(dictionary))
    query_doc = [w.lower() for w in word_tokenize(query)]
    query_doc_bow = dictionary.doc2bow(query_doc)
    query_doc_tf_idf = tf_idf[query_doc_bow]
    return(sims[query_doc_tf_idf])

def sim_func3(query, corpus_of_documents):
    nlp = spacy.load('en_core_web_sm')
    sims = []
    for document in corpus_of_documents:
        query = nlp(query)
        document = nlp(document)
        sims.append(query.similarity(document))
    return sims

def sim_func4(query, corpus_of_documents):
    stemmer = nltk.stem.porter.PorterStemmer()
    remove_punctuation_map = dict((ord(char), None) for char in string.punctuation)

    def stem_tokens(tokens):
        return [stemmer.stem(item) for item in tokens]
    
    '''remove punctuation, lowercase, stem'''
    def normalize(text):
        return stem_tokens(nltk.word_tokenize(text.lower().translate(remove_punctuation_map)))
    
    vectorizer = TfidfVectorizer(tokenizer=normalize, stop_words='english')
    sims = []
    for document in corpus_of_documents:
        tfidf = vectorizer.fit_transform([query, document])
        sims.append(((tfidf * tfidf.T).A)[0,1])
    return sims

enabled_similarity_functions:list[Callable] = [sim_func1, sim_func2, sim_func3, sim_func4]

def return_response(tours, corpus_of_documents, query):
    similarities = []
    for document in corpus_of_documents:
        similarity = sim_func1(query, document)
        similarities.append(similarity)
        tour_id = similarities.index(max(similarities))
    return tour_id, corpus_of_documents[similarities.index(max(similarities))]
