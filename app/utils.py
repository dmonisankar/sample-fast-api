import uuid

def generate_unique_id(length: int = 8) -> str:
    """Generate a unique alphanumeric ID of given length."""
    unique_id = uuid.uuid4().hex  # Get a random UUID and convert to a hex string
    return unique_id[:length]  # Return the first 'length' characters