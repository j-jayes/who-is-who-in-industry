# Purpose

# We want to assign hiscos to every occupation so that we can look at occupational upgrading and those individuals who lived in the USA
# In order to do so we will use the openai embeddings to find the occupations closest in the embedding space to the hiscos.
# we scrape the hiscos and their descriptions from the hisco website
# then we preprocess the descriptions and get the embeddings
# then we get the embeddings for the hiscos
# then we find the closest occupations to the hiscos
# then we assign the hiscos to the closest occupations


import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd

# Download stopwords if you haven't already
nltk.download('stopwords')
nltk.download('wordnet')

# Initialize lemmatizer and stopwords list
lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words('english'))

# Define a preprocessing function
def preprocess(text):
    words = nltk.word_tokenize(text)
    words = [lemmatizer.lemmatize(word) for word in words if word.isalnum() and word not in stop_words]
    return ' '.join(words)

# read in data from "data/occupations/3-digit-occupations.csv"
df = pd.read_csv('data/occupations/3-digit-occupations.csv')
df['first_digit'] = df['Number'].apply(lambda x: int(str(x)[0]))


# Apply the preprocessing function to the DataFrame
df['processed_description'] = df['Description (tasks and duties)'].apply(preprocess)

# remove "Workers unit group" from processed_description
df['processed_description'] = df['processed_description'].apply(lambda x: x.replace('Workers unit group', ''))

# remove "Specialisatio Unkown" from Name, as well as "Not Elsewhere Classified"
df['Name'] = df['Name'].apply(lambda x: x.replace('Specialisation Unknown', ''))
df['Name'] = df['Name'].apply(lambda x: x.replace('Not Elsewhere Classified', ''))

# concatenate Name and processed_description into a new column called "hisco_text"
df['hisco_text'] = df['Name'] + ' ' + df['processed_description']


import openai
import yaml

with open('config.yaml', 'r') as f:
    config = yaml.safe_load(f)

openai.api_key = config['default']['key']

def get_embedding(text, model="text-embedding-ada-002"):
    text = text.replace("\n", " ")
    return openai.Embedding.create(input=[text], model=model)['data'][0]['embedding']

# Apply the get_embedding function to your 'hisco_text' column
df['ada_embedding'] = df['hisco_text'].apply(lambda x: get_embedding(x, model='text-embedding-ada-002'))

# save embeddings dataset
df.to_excel('data/occupations/3-digit-occupations_with_embeddings.xlsx')