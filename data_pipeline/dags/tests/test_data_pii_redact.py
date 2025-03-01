import unittest
from presidio_analyzer import RecognizerResult
from scripts.data_preprocessing.check_pii_data import PIIHandler

class TestPIIHandler(unittest.TestCase):
    
    def setUp(self):
        """Initialize the PIIHandler before each test."""
        self.pii_handler = PIIHandler()
    
    def test_detect_pii_direct_identifiers(self):
        """Test detection of direct identifiers."""
        text = "John Doe's email is johndoe@example.com and his SSN is 847-43-3423."
        pii_data, _ = self.pii_handler.detect_pii(text)
        
        self.assertIn('EMAIL_ADDRESS', pii_data)
        self.assertIn('US_SSN', pii_data)
        self.assertEqual(pii_data['EMAIL_ADDRESS'][0], 'johndoe@example.com')
        self.assertEqual(pii_data['US_SSN'][0], '847-43-3423')
    
    def test_detect_pii_sensitive_data(self):
        """Test detection of sensitive financial data."""
        text = "My credit card number is 4111-1111-1111-1111."
        pii_data, _ = self.pii_handler.detect_pii(text)
        
        self.assertIn('CREDIT_CARD', pii_data)
        self.assertEqual(pii_data['CREDIT_CARD'][0], '4111-1111-1111-1111')
    
    def test_detect_pii_corporate_data(self):
        """Test detection of corporate confidential data."""
        text = "Employee ID: EMP12345. Salary: $100,000."
        pii_data, _ = self.pii_handler.detect_pii(text)
        
        self.assertIn('CORPORATE_DATA', pii_data)
    
    def test_detect_pii_it_security_data(self):
        """Test detection of IT security credentials."""
        text = "API key: sk_test_abcdef123456."
        pii_data, _ = self.pii_handler.detect_pii(text)
        
        self.assertIn('SECURITY_DATA', pii_data)
    
    def test_redact_pii(self):
        """Test redaction of detected PII."""
        text = "John Doe's email is johndoe@example.com and his SSN is 847-43-3423."
        pii_data, results = self.pii_handler.detect_pii(text)
        redacted_text = self.pii_handler.redact_pii(text, results)
        
        self.assertNotIn('johndoe@example.com', redacted_text)
        self.assertNotIn('123-45-6789', redacted_text)
    
    def test_empty_text(self):
        """Test handling of empty text."""
        text = ""
        pii_data, results = self.pii_handler.detect_pii(text)
        redacted_text = self.pii_handler.redact_pii(text, results)
        
        self.assertEqual(pii_data, {})
        self.assertEqual(redacted_text, "")
    
    def test_no_pii(self):
        """Test handling of text with no PII."""
        text = "Hello, this is a sample text with no PII."
        pii_data, results = self.pii_handler.detect_pii(text)
        redacted_text = self.pii_handler.redact_pii(text, results)
        
        self.assertEqual(pii_data, {})
        self.assertEqual(redacted_text, text)
    
if __name__ == '__main__':
    unittest.main()
