from pydantic_ai import Agent
from pydantic_ai.models.google import GoogleModel
from pydantic_ai.providers.google import GoogleProvider


import os
import sys
sys.stdout.reconfigure(encoding='utf-8')
import json

#dependencies
from dependencies import input_manager
from dependencies import JSON_extractor

#agents
from agents.content_praser import content_praser
from agents.senti_analyser import sent_analysis
from agents.insight import insi_analysis

#dependencies instantiation 
input_parse = input_manager.input_manager()
json_extractor = JSON_extractor.extract_json()

#agents instantiation
content_praser = content_praser()
sentiment_agent = sent_analysis()
insights = insi_analysis()

#we can add an empty space. allowing the users to upload a file in that space. And refer to the file in that space. 
filepath = r"C:\Users\ojas2\OneDrive\Desktop\TUF\b.tech\data_sciences\Project\Finance_news_analysis\trial.json"
absolute_path = os.path.abspath(filepath)

article_id, headline, content, timestamp = input_parse.load_json_as_dict( file_path=absolute_path)


assert type(content) == str
output = sentiment_agent.respond(content)

insights_out = insights.respond(output)
insights_out = insights_out[7:-4]
try:
    output_dict = json.loads(insights_out)

    # Now you can use output_dict like a regular Python dictionary
    print(f"Type of output_dict: {type(output_dict)}")
    print(f"Insights: {output_dict['insights']}")
    print(f"First insight: {output_dict['insights'][0]}")
    print(f"Score: {output_dict['score']}")

except json.JSONDecodeError as e:
    print(f"Error decoding JSON: {e}")
    print("Please ensure the string is valid JSON format.")
except KeyError as e:
    print(f"KeyError: {e} - The expected key was not found in the dictionary.")
