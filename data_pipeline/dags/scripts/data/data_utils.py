import re
import string

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

def clean_text(text):
    """Clean and standardize text."""
    text = text.strip()
    text = ''.join(e for e in text if e.isalnum() or e.isspace() or e in string.punctuation)
    text = text.lower()
    return text