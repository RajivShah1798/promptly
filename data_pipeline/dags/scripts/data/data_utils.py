import re
import string
import nltk
from nltk.tokenize import word_tokenize
# from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from autocorrect import Speller
from airflow.operators.python import get_current_context

# Download necessary NLTK resources
# nltk.download('punkt')
# # nltk.download('stopwords')
# nltk.download('wordnet')

# Initialize components
lemmatizer = WordNetLemmatizer()
spell = Speller(lang='en')
# stop_words = set(stopwords.words('english'))

def remove_punctuation(text):
    """
    Remove all punctuation from a given text.

    Parameters
    ----------
    text : str
        The text from which to remove punctuation.

    Returns
    -------
    str
        The input text with all punctuation removed.
    """
    punts = string.punctuation
    new_text = ''.join(e for e in text if e not in punts)
    return new_text


def clean_text_using_lemmatizer(text):
    """Cleans and preprocesses user queries."""
    nltk.download("wordnet") 
    
    from nltk.corpus import wordnet

    # Convert to lowercase
    text = text.lower()
    
    # Remove URLs
    text = re.sub(r'https?://\S+|www\.\S+', '', text)
    
    # Remove special characters, numbers, and punctuation
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    
    # Tokenization
    tokens = word_tokenize(text)
    
    # Lemmatization
    tokens = [lemmatizer.lemmatize(word) for word in tokens]
    
    # Optional: Spell Correction (Can be removed if latency is a concern)
    tokens = [spell(word) for word in tokens]
    
    return ' '.join(tokens)


def clean_response(response):
    """Remove leading index numbers from a response."""
    
    unwanted_patterns = [
        r'positive neutral negative.*?sentiment score',
        r'percent of sentiment.*?sentiment score'
    ]
    
    # Apply each unwanted pattern removal
    for pattern in unwanted_patterns:
        response = re.sub(pattern, '', response, flags=re.IGNORECASE | re.DOTALL).strip()
    
    response = re.sub(r"^\d+\s*", "", response.strip())
    # remove next line characters
    response = response.replace("\n", " ")
    response = response.replace("\r", " ")
    response = response.replace("\t", " ")
    return response


def check_xcom_data(ti):
    context = get_current_context()

    queries = context['ti'].xcom_pull(task_ids='get_supabase_data', key='get_initial_queries')
    quer2 = ti.xcom_pull(task_ids='get_supabase_data', key='get_initial_queries')

    print("XCom Data 222:", queries)
    print("XCom DDD:", quer2)


def clean_text(queries):
    """Clean and standardize text."""

    if queries is None:
        raise ValueError("No data found in XCom! Ensure 'get_supabase_data' ran successfully.")

    cleaned_queries = [clean_text_using_lemmatizer(q['query']) for q in queries]
    cleaned_responses = [clean_text_using_lemmatizer(r['response']) for r in queries]

    print(cleaned_queries)
    print(cleaned_responses)

    # context['ti'].xcom_push(key='lemmatized_user_queries', value=cleaned_queries)
    # context['ti'].xcom_push(key='lemmatized_user_responses', value=cleaned_responses)

    return [cleaned_queries, cleaned_responses]