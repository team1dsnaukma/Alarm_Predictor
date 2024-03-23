import regex as re
import calendar
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl

import nltk
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords


def to_vector_preprocessing(text, stop_words=[]):
    if not stop_words:
        stop_words = stopwords.words("english")
    lemmatizer = WordNetLemmatizer()
    text_array = word_tokenize(re.sub('[\W\s\d]', ' ', text.lower()))
    processed_text = ' '.join(
            [
            word for word in text_array
            if (len(word) > 2) and (word not in stop_words)
            ])
    return processed_text


def tfidf_vectorizer(_corpus):
    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(_corpus)
    sparse_matrix = pd.DataFrame(X.todense(), columns=vectorizer.get_feature_names())
    return sparse_matrix


def plot_top_by_doc(df, n=5):
    fig, ax = plt.subplots(n, figsize=(6, 30))
    for i in range(n):
        df.iloc[i, :].sort_values(ascending=False)[:10].plot.barh(
            ax=ax[i],
            cmap="jet",
            title=f"Doc {i}").invert_yaxis()
    plt.subplots_adjust(hspace=0.4)