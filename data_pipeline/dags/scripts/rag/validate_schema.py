def validate_rag_schema(data: dict) -> dict:
    """
    Validate the schema of the chunked document data.

    Args:
        data (dict): A dictionary where keys are file names and values are lists of text chunks.

    Raises:
        ValueError: If validation fails for any file_name or chunk.

    Returns:
        dict: Validated chunked data.
    """
    try:
        if not isinstance(data, dict):
            raise ValueError("Input data must be a dictionary.")
        
        for file_name, chunks in data.items():
            # Validate file_name
            if not isinstance(file_name, str) or not file_name.strip():
                raise ValueError(f"Validation failed: 'file_name' must be a non-empty string. Found: {file_name}")

            # Validate chunks
            if not isinstance(chunks, list) or not chunks:
                raise ValueError(f"Validation failed: 'chunks' must be a non-empty list for file: {file_name}")
            
            for idx, chunk in enumerate(chunks):
                if not isinstance(chunk, str) or not chunk.strip():
                    raise ValueError(f"Validation failed: Empty or invalid chunk at index {idx} for file: {file_name}")

        return data

    except Exception as e:
        print(f"An error occurred during schema validation: {e}")
        raise RuntimeError("Failed to validate RAG schema.") from e