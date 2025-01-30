import joblib
import re
import string
import numpy as np
import joblib
from nltk.corpus import stopwords
import nltk
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
nltk.download('stopwords')
nltk.download('punkt_tab')
def preprocess_text(text):
    text = str(text)
    stop_words = set(stopwords.words('english'))
    stemmer = PorterStemmer()
    text = text.lower()
    url_pattern = re.compile(r'https?://\S+|www\.\S+')
    text = url_pattern.sub(' ', text)
    text = re.sub(r'<.*?>', '', text)
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    filtered_words = [word for word in text.split() if word not in stop_words]
    contractions = r"(\b(?:U\.S|Dr|Mrs|Mr|i\.e|e\.g)\.|\b(?:I'm|you're|they're|it's|doesn't|didn't)\b)"
    text = re.sub(contractions, lambda x: x.group(0).replace('.', '<PERIOD>'), text)
    text = text.translate(str.maketrans('', '', string.punctuation))
    text = text.replace('<PERIOD>', '.')
    tokens = word_tokenize(text)

    stemmed_words = [stemmer.stem(word) for word in filtered_words]

    return ' '.join(stemmed_words)



def get_sentence_embedding(model,sentence):
    words=sentence.split()
    # Access word vectors using model.wv[word]
    word_vectors=[model.wv[word] for word in words if word in model.wv]
    if len(word_vectors)>0:
        sentence_embedding=np.mean(word_vectors,axis=0)
    else:
        sentence_embedding=np.zeros(model.vector_size)
    return sentence_embedding
def predict_sentiment(sentence):
    logistic_model=joblib.load('../models/logistic_model.pkl')
    word2vec_model=joblib.load('../models/word2vec.model')
    sentence=preprocess_text(sentence)
    sentence_embedding=get_sentence_embedding(word2vec_model,sentence)
    sentence_embedding=sentence_embedding.reshape(1,-1)
    sentiment=logistic_model.predict(sentence_embedding)
    return sentiment[0]