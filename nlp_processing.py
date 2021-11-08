import pandas as pd
import json as j
import numpy as np
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction import SelectKBest, chi2
import pickle


example_words = ["python", "pythoner", "pythoning", "pythoned", "pythonly"]

def nlp_filter(csv_file):
         print(csv_file)

