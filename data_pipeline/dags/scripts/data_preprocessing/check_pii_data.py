"""
To ensure compliance for PII data in any documents uploaded by our users, we will be implementing the
following:

    1. Notify the user about the presence of PII in the document uploaded.
    2. Provide the user with the option to either cancel the upload of the document, redact PII data, 
    or authorize usage of data with PII intact (If authorized, Promptly shall not be responsible for consequences)
    3. As per GDPR standards, we will be handling the following set of PII information:
        i.   Direct Identifiers: Names, Email Address, Phone numbers, Address, National ID numbers (SSN, ITIN, Aadhaar, PAN).
        ii.  Sensitive data: Financial Data(credit/debit card numbers), bank account numbers
        iii. Corporate Confidential Data: Employee Records, Salaries, etc.
        iv.  IT and System Security Data: User credentials, API Keys, Tokens, IP Addresses.
    4. While Promptly will try to redact sensitive information, the redaction may not be absolute. Promptly 
    shall bear no liability incase of data leakage. We therefore, recommend uploading documents without the presence of PII
"""


# Imports
from presidio_analyzer import AnalyzerEngine, Pattern, PatternRecognizer, RecognizerResult
from presidio_anonymizer import AnonymizerEngine
from typing import List, Dict, Tuple
import logging

logging.basicConfig(level=logging.INFO)


class CorporateDataRecognizer(PatternRecognizer):
    """Detect corporate confidential data like salaries and employee records."""
    def __init__(self):
        patterns = [
            Pattern("SALARY", r'(?i)\b(?:salary|compensation|pay|income|bonus)\b[\s:\-]*(?:is|was|around|about|approximately|near)?[\s:\-]*\(?[$€£₹]?(?:USD|INR|EUR)?\s?\d{1,3}(?:,\d{3})*(?:\.\d{1,2})?[KMB]?\b', 0.95),
            Pattern("EMPLOYEE_RECORD", r'(?i)\b(employee\s+id|hr\s+record|staff\s+id)\b(?:\s*(?:number)?)?\s*(?:is|:|=)?\s*([\w-]+)', 0.8)
        ]
        super().__init__(supported_entity="CORPORATE_DATA", patterns=patterns)

class ITSecurityRecognizer(PatternRecognizer):
    """Detect IT security data like API keys, tokens, and credentials."""
    def __init__(self):
        patterns = [
            Pattern("API_KEY", r'(?i)\b(api[\s_-]?key|token|jwt|bearer|session[\s_-]?id|access[\s_-]?token|auth[\s_-]?token|refresh[\s_-]?token)\b\s*(?:is|=|:)?\s*([\w-]+\.?[\w-]*\.?[\w-]*)', 0.9),
            Pattern("CREDENTIALS", r'(?i)\b(username|user|login|credential|password|pwd)\b\s*(?:is|:|=)?\s*([\S]+)', 0.9)
        ]
        super().__init__(supported_entity="SECURITY_DATA", patterns=patterns)

class PIIHandler:
    """Handle PII Data. Carry out both detection as well as redaction of PII"""
    def __init__(self) -> None:
        self.direct_idents = ['PERSON', 'LOCATION', 'PHONE_NUMBER', \
            'EMAIL_ADDRESS', 'US_SSN', 'US_ITIN', 'US_PASSPORT', 'US_DRIVER_LICENSE',\
                'IN_AADHAAR', 'IN_PASSPORT', 'IN_PAN', '']
        self.sensitive_data = ['IBAN_CODE', 'CREDIT_CARD', 'US_BANK_NUMBER']
        self.corporate_data = ['CORPORATE_DATA']
        self.it_sec_data = ['IP_ADDRESS', 'SECURITY_DATA']
        
        self.analyzer = AnalyzerEngine()
        self.analyzer.registry.add_recognizer(CorporateDataRecognizer())
        self.analyzer.registry.add_recognizer(ITSecurityRecognizer())
        self.anonymizer = AnonymizerEngine()
        
    def detect_pii(self, text: str) -> Tuple[Dict[str, List[str]], List[RecognizerResult]]:
        result = self.analyzer.analyze(text=text, \
            entities = self.direct_idents + self.sensitive_data + self.corporate_data + self.it_sec_data, \
                language='en')
        pii_data = {}
        for pii in result:
            entity_type = pii.entity_type
            if entity_type not in pii_data:
                pii_data[entity_type] = []
            pii_data[entity_type].append(text[pii.start:pii.end])
        return (pii_data, result)
            
    def redact_pii(self, text: str, detected_pii: List[RecognizerResult]):
        redacted_text = self.anonymizer.anonymize(text, analyzer_results=detected_pii)
        
        return redacted_text.text


def check_for_pii(documents):
    """
    Detects PII in multiple documents.

    Args:
        documents (list of dict): Each dictionary contains 'filename' and 'text'.

    Returns:
        list of dict: Each dictionary contains 'filename', 'text', and 'pii_results'.
    """
    pii_handler = PIIHandler()
    processed_documents = []

    for filename, text in documents.items():
        # filename = doc.get('filename')
        # text = doc.get('text')
        
        # Detect PII in the text
        pii_data, results = pii_handler.detect_pii(text)

        print('filename', filename)
        print('text', text)
        print('pii_results', results)
        print('pii_detected', pii_data)
        
        processed_documents.append({
            'filename': filename,
            'text': text,
            'pii_results': results, 
            'pii_detected': pii_data
        })
    
    logging.info("Checked for PII. Documents along with their PII Results are available")
    return processed_documents


def redact_pii(documents_with_pii):
    """
    Redacts PII in multiple documents.

    Args:
        documents_with_pii (list of dict): Each dictionary contains 'filename', 'text', and 'pii_results'.

    Returns:
        list of dict: Each dictionary contains 'filename' and 'redacted_text'.
    """
    pii_handler = PIIHandler()
    redacted_documents = []

    for doc in documents_with_pii:
        filename = doc.get('filename')
        text = doc.get('text')
        pii_results = doc.get('pii_results')
        
        # Redact PII in the text
        redacted_text = pii_handler.redact_pii(text, pii_results)

        print('filename', filename)
        print('Redacted text', redacted_text)
        
        # redacted_documents.append({
        #     'filename': filename,
        #     'redacted_text': redacted_text
        # })
        redacted_documents.append({
            filename: redacted_text
        })
    
    logging.info("PII redaction step executed. All Documents are be PII complaint now ")
    return redacted_documents

if __name__=='__main__':
    document_text = "John Doe's salary is $120,000. API key: sk_live_123456789abcdefghij."
    pii_handler = PIIHandler()
    pii_data, results = pii_handler.detect_pii(document_text)
    redacted_text = pii_handler.redact_pii(document_text, results)
    print("Detected PII Data: ", pii_data)
    print("Original Text: ", document_text)
    print("Redacted Text: ", redacted_text)