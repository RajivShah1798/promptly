import unittest
from scripts.data_preprocessing.data_utils import clean_text_using_lemmatizer, clean_text

class TestTextCleaning(unittest.TestCase):

    def setUp(self):
        self.sample_queries = [
            {
                'query': 'Check the price at https://example.com!',
                'response': 'The cost is $120.',
                'context': 'Product price check on 2021-12-31.'
            },
            {
                'query': 'HELLO WORLD!!!',
                'response': 'Greetings!',
                'context': 'User greeted the system.'
            }
        ]

    def test_clean_text_using_lemmatizer(self):
        text = 'Running quickly to the stores at https://shop.com'
        cleaned_text = clean_text_using_lemmatizer(text)

        # Ensure URLs are removed
        self.assertNotIn('https://shop.com', cleaned_text)

        # Ensure text is lowercase
        self.assertTrue(cleaned_text.islower())

        # Ensure special characters are removed
        self.assertNotIn('!', cleaned_text)

        # Ensure lemmatization (e.g., "running" becomes "run")
        self.assertIn('run', cleaned_text)

    def test_clean_text(self):
        cleaned_data = clean_text(self.sample_queries)

        # Check structure
        self.assertEqual(len(cleaned_data), 3)

        cleaned_queries, cleaned_responses, cleaned_contexts = cleaned_data

        # Ensure each query, response, and context is cleaned
        self.assertEqual(len(cleaned_queries), len(self.sample_queries))

        # Validate cleaned content
        self.assertIn('check the price', cleaned_queries[0])
        self.assertIn('the cost is', cleaned_responses[0])
        self.assertIn('product price check', cleaned_contexts[0])

    def test_clean_text_with_none_input(self):
        with self.assertRaises(ValueError) as context:
            clean_text(None)

        self.assertEqual(str(context.exception), "No data found in XCom! Ensure 'get_supabase_data' ran successfully.")

if __name__ == '__main__':
    unittest.main()