import unittest
from unittest.mock import patch, MagicMock
import pandas as pd

from scripts.rag.rag_utils import chunk_text, embed_and_store_chunks

class TestRAGPipeline(unittest.TestCase):

    def test_chunk_text_basic(self):
        input_text = "This is a long text that needs to be chunked. It has multiple sentences to test the chunking logic."
        chunk_size = 20

        chunks = chunk_text(input_text, chunk_size)

        self.assertIsInstance(chunks, list)
        self.assertGreater(len(chunks), 0)
        for chunk in chunks:
            self.assertLessEqual(len(chunk), chunk_size)

    def test_chunk_text_empty(self):
        chunks = chunk_text("", 50)

        self.assertEqual(chunks, [])

    def test_chunk_text_large_chunk_size(self):
        input_text = "Short text."
        chunk_size = 100

        chunks = chunk_text(input_text, chunk_size)

        self.assertEqual(len(chunks), 1)
        self.assertEqual(chunks[0], input_text)

    @patch("scripts.rag_pipeline.generate_embeddings")
    @patch("scripts.rag_pipeline.store_embeddings_in_supabase")
    def test_embed_and_store_chunks_success(self, mock_store, mock_generate):
        # Mock the embedding generation and storage
        mock_generate.return_value = [[0.1, 0.2, 0.3]]

        # Input data
        chunks = ["Test chunk"]
        metadata = {"document_id": "123"}

        embed_and_store_chunks(chunks, metadata)

        mock_generate.assert_called_once_with(chunks)
        mock_store.assert_called_once()

        # Check the passed data
        stored_data = mock_store.call_args[0][0]
        self.assertEqual(stored_data[0]['text'], "Test chunk")
        self.assertEqual(stored_data[0]['embedding'], [0.1, 0.2, 0.3])
        self.assertEqual(stored_data[0]['metadata'], metadata)

    @patch("scripts.rag_pipeline.generate_embeddings")
    @patch("scripts.rag_pipeline.store_embeddings_in_supabase")
    def test_embed_and_store_chunks_empty(self, mock_store, mock_generate):
        chunks = []
        metadata = {"document_id": "123"}

        embed_and_store_chunks(chunks, metadata)

        mock_generate.assert_not_called()
        mock_store.assert_not_called()

    @patch("scripts.rag_pipeline.generate_embeddings", side_effect=Exception("Embedding Error"))
    def test_embed_and_store_chunks_embedding_failure(self, mock_generate):
        chunks = ["Test chunk"]
        metadata = {"document_id": "123"}

        with self.assertRaises(Exception) as context:
            embed_and_store_chunks(chunks, metadata)

        self.assertEqual(str(context.exception), "Embedding Error")

if __name__ == '__main__':
    unittest.main()
