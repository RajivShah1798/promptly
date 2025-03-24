def validate_schema(data: list) -> list:
    """
    Validate the schema of the data.

    Args:
    data (list): List of dictionaries containing 'Query', 'Context', and 'Response' keys.

    Raises:
    ValueError: If the schema validation fails for any item in the data.
    """
    try:
        for idx, item in enumerate(data):
            # Ensure that each dictionary item contains the required keys
            if 'query' not in item or 'response' not in item:
                raise ValueError(f"Validation failed for item at index {idx}: Missing required keys.")
            # Check if the Query key is a non-empty string
            if not isinstance(item['query'], str) or not item['query'].strip():
                raise ValueError(f"Validation failed for item at index {idx}: Invalid or empty 'Query' value.")
            # Check if the Response key is a non-empty string
            if not isinstance(item['response'], str) or not item['response'].strip():
                raise ValueError(f"Validation failed for item at index {idx}: Invalid or empty 'Response' value.")
        return data
    except Exception as e:
        print(f"An error occurred during schema validation: {e}")
        raise RuntimeError("Failed to validate schema.") from e