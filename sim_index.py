import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from dependencies import input_manager, JSON_extractor

import os
import json
analyzer = SentimentIntensityAnalyzer()

input_parse = input_manager.input_manager()
json_extractor = JSON_extractor.extract_json()

filepath = r"C:\Users\ojas2\OneDrive\Desktop\TUF\b.tech\data_sciences\Project\Finance_news_analysis\trial.json"
absolute_path = os.path.abspath(filepath)
article_id, headline, content, timestamp = input_parse.load_json_as_dict( file_path=absolute_path)


vs1 = analyzer.polarity_scores(content)

from agents.senti_analyser import   sent_analysis
analyzer_2 = sent_analysis()
vs_out = analyzer_2.respond(content)
vs_out = vs_out[7:-4]

data_dict = json.loads(vs_out)
data = data_dict[0]
print(data.get('score'))
print(vs1.get('compound'))

validation = (data.get('score') - vs1.get('compound')) / (data.get('score') + vs1.get('compound'))

print(f"final validation error is {validation}")

