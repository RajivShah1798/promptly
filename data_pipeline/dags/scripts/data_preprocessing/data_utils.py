import re
import string
import nltk
from nltk.tokenize import word_tokenize
# from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from autocorrect import Speller
from airflow.operators.python import get_current_context

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


def clean_text(queries):
    """Clean and standardize text."""

    if queries is None:
        raise ValueError("No data found in XCom! Ensure 'get_supabase_data' ran successfully.")

    cleaned_queries = [clean_text_using_lemmatizer(q['query']) for q in queries]
    cleaned_responses = [clean_text_using_lemmatizer(r['response']) for r in queries]
    cleaned_context = [clean_text_using_lemmatizer(c['context']) for c in queries]

    print(cleaned_queries)
    print(cleaned_responses)
    print(cleaned_context)

    return [cleaned_queries, cleaned_responses, cleaned_context]