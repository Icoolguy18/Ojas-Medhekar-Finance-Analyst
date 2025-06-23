import json
import os
import sys
sys.stdout.reconfigure(encoding='utf-8')

class input_manager:
    def __init__(self, source_type="file"):
        self.source_type = source_type
        print(f"InputManager initialized with source: {self.source_type}")

    def load_json_as_dict(self, file_path: str):
        if not os.path.exists(file_path):
            print(f"Error: File not found at '{file_path}'")
            return None, None, None, None

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            if not isinstance(data, dict):
                print(f"Error: JSON root element is not a dictionary.")
                return None, None, None, None

            article_id = data.get("article_id")
            headline = data.get("headline")
            content = data.get("content")
            published_at = data.get("published_at")

            return article_id, headline, content, published_at

        except json.JSONDecodeError as e:
            print(f"Error decoding JSON from '{file_path}': {e}")
            return None, None, None, None
        except Exception as e:
            print(f"An unexpected error occurred while reading '{file_path}': {e}")
            return None, None, None, None
