import string
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
import re
import unidecode
import spacy
import numpy as np
import pandas as pd

nlp = spacy.load("fr_core_news_sm")


def preprocess(text,
               punctuation=False,
               lower_case=True,
               remove_stopwords=False,
               accents=True,
               numbers=True,
               lemmatize=False,
               language='french'):

    if punctuation:
        text = ''.join(char for char in text if not char in string.punctuation)
    if lower_case:
        text = text.lower()
    if numbers:
        text = ''.join(char for char in text if not char.isdigit())
    if accents:
        text = unidecode.unidecode(text)
    if remove_stopwords:
        stop_words = set(stopwords.words(language))
        word_tokens = word_tokenize(text)
        text = ' '.join(char for char in word_tokens if not char in stop_words)
    if lemmatize:
        text = word_tokenize(text)
        lemmatizer = WordNetLemmatizer()
        lemmatized = [lemmatizer.lemmatize(char) for char in text]
        text = ' '.join(lemmatized)
    return text


def add_cleaned_column(df):
    df["preprocess_data"] = df['text'].apply(lambda x: preprocess(x))
    return df


def return_token(sentence):
    # Tokeniser la phrase
    doc = nlp(sentence)
    # Retourner le texte de chaque token
    return [X.text for X in doc]


def return_word_embedding(sentence):
    # Vectoriser la phrase
    doc = nlp(sentence)
    # Retourner le vecteur lié à chaque token
    return [(X.vector) for X in doc]


def stopword_count(text):
    stop_words = set(stopwords.words('french'))
    word_tokens = word_tokenize(text)
    stopword_count = len([w for w in word_tokens if w in stop_words])
    return stopword_count


def vocab_richness(text):
    tokens = word_tokenize(text)
    total_length = len(tokens)
    unique_words = set(tokens)
    unique_word_length = len(unique_words)
    return unique_word_length / total_length


def features(df):
    df['preprocess_data'] = df['text'].apply(lambda x: preprocess(x))
    df['word_count'] = df['text'].apply(lambda x: len(x.split()))
    df['unique_word_count'] = df['text'].apply(
        lambda x: len(np.unique(x.split())))
    df['sentences_count'] = df['text'].apply(lambda x: x.count('.'))
    df['stopwords_count'] = df['text'].apply(lambda x: stopword_count(x))
    df['vocab richness'] = df['text'].apply(vocab_richness)
    return df
