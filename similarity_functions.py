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

nltk.download('punkt')

def jaccard_similarity(query, document):
    query = query.lower().split(" ")
    document = document.lower().split(" ")
    intersection = set(query).intersection(set(document))
    union = set(query).union(set(document))
    return len(intersection)/len(union)

stemmer = nltk.stem.porter.PorterStemmer()
remove_punctuation_map = dict((ord(char), None) for char in string.punctuation)

def stem_tokens(tokens):
    return [stemmer.stem(item) for item in tokens]

'''remove punctuation, lowercase, stem'''
def normalize(text):
    return stem_tokens(nltk.word_tokenize(text.lower().translate(remove_punctuation_map)))

vectorizer = TfidfVectorizer(tokenizer=normalize, stop_words='english')

def cosine_sim(text1, text2):
    tfidf = vectorizer.fit_transform([text1, text2])
    return ((tfidf * tfidf.T).A)[0,1]

def gensim(text1, text2, corpus_of_documents = corpus_of_documents):
    gen_docs = [[w.lower() for w in word_tokenize(text1)]
        for text in corpus_of_documents]
    dictionary = gensim.corpora.Dictionary(gen_docs)
    corpus = [dictionary.doc2bow(gen_doc) for gen_doc in gen_docs]
    tf_idf = gensim.models.TfidfModel(corpus)
    sims = gensim.similarities.Similarity('workdir/',tf_idf[corpus], num_features=len(dictionary))
    query_doc = [w.lower() for w in word_tokenize(text2)]
    query_doc_bow = dictionary.doc2bow(query_doc)
    query_doc_tf_idf = tf_idf[query_doc_bow]
    return(sims[query_doc_tf_idf])

def return_response(sim_func, query, corpus):
    similarities = []
    for doc in corpus:
        similarity = sim_func(user_input, doc)
        print(similarity)
        similarities.append(similarity)
        tour_id = similarities.index(max(similarities))
    return tour_id, corpus_of_documents[similarities.index(max(similarities))]