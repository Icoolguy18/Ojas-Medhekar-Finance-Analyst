import json

class extract_json:
    def extract_json_from_output(self, model_output_string: str) -> str:
        assert type(model_output_string) == str
        start_delimiter = "```json"
        end_delimiter = "```"

        if model_output_string.startswith(start_delimiter):
            json_content = model_output_string[len(start_delimiter):].strip()
        else:
            json_content = model_output_string.strip() # good to strip general whitespace

        if json_content.endswith(end_delimiter):
            json_content = json_content[:-len(end_delimiter)].strip()
            
        try:
            parsed_json_output = json.loads(json_content)
            return parsed_json_output
        except json.JSONDecodeError as e:
            print(f"Error: Could not decode JSON from extracted string. Error: {e}")
            print(f"Attempted to decode: '{json_content}'")
            return None 
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return None
        
        assert type(json_content) == dict 
        
        return json_content