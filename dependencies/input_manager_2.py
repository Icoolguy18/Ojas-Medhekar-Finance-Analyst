import json
import os
import sys

# Ensures console output is correctly encoded, especially for special characters
sys.stdout.reconfigure(encoding='utf-8')

class InputManager:
    def __init__(self, source_type="file"):
        self.source_type = source_type
        print(f"InputManager initialized with source: {self.source_type}")

    def _extract_article_data(self, data_dict: dict) -> tuple:
        """
        Private helper method to extract specific article data fields from a dictionary.
        This method assumes the input 'data_dict' is already a valid Python dictionary.
        """
        if not isinstance(data_dict, dict):
            print(f"Error: Expected a dictionary for data extraction, but received {type(data_dict).__name__}.")
            return None, None, None, None

        # Using .get() provides a safe way to access keys, returning None if the key doesn't exist.
        article_id = data_dict.get("article_id")
        headline = data_dict.get("headline")
        content = data_dict.get("content") # Ensure your JSON key is "content", not "conetnt"
        published_at = data_dict.get("published_at")

        return article_id, headline, content, published_at

    def load_from_file(self, file_path: str) -> tuple:
        """
        Loads JSON content from a specified file path and extracts article data.
        
        Args:
            file_path (str): The absolute or relative path to the JSON file.

        Returns:
            tuple: A tuple containing (article_id, headline, content, published_at).
                   Returns (None, None, None, None) if the file is not found,
                   JSON is invalid, or an unexpected error occurs.
        """
        print(f"Attempting to load from file: {file_path}")
        if not os.path.exists(file_path):
            print(f"Error: File not found at '{file_path}'")
            return None, None, None, None

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                # json.load() reads directly from the file object and parses to a Python object
                raw_data = json.load(f)
            
            # Now, pass the parsed Python object to the common extraction method
            return self._extract_article_data(raw_data)

        except json.JSONDecodeError as e:
            print(f"Error decoding JSON from '{file_path}': {e}")
            return None, None, None, None
        except Exception as e:
            print(f"An unexpected error occurred while reading file '{file_path}': {e}")
            return None, None, None, None

    def process_direct_dict_input(self, input_data_dict: dict) -> tuple:
        """
        Processes a Python dictionary directly and extracts article data.
        
        Args:
            input_data_dict (dict): A Python dictionary containing the article data.

        Returns:
            tuple: A tuple containing (article_id, headline, content, published_at).
                   Returns (None, None, None, None) if the input is not a dictionary
                   or expected keys are missing.
        """
        print("Processing direct dictionary input...")
        # Directly pass the dictionary to the common extraction method
        return self._extract_article_data(input_data_dict)

    def process_json_string_input(self, json_string: str) -> tuple:
        """
        Processes a raw JSON formatted string and extracts article data.
        
        Args:
            json_string (str): A string containing valid JSON.

        Returns:
            tuple: A tuple containing (article_id, headline, content, published_at).
                   Returns (None, None, None, None) if the string is not valid JSON
                   or expected keys are missing.
        """
        print("Processing raw JSON string input...")
        try:
            # First, parse the JSON string into a Python dictionary
            raw_data = json.loads(json_string)
            # Then, pass the parsed dictionary to the common extraction method
            return self._extract_article_data(raw_data)
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON string: {e}")
            return None, None, None, None
        except Exception as e:
            print(f"An unexpected error occurred while processing JSON string: {e}")
            return None, None, None, None