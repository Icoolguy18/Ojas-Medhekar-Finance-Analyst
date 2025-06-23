from pydantic_ai import Agent
from pydantic_ai.models.google import GoogleModel
from pydantic_ai.providers.google import GoogleProvider

import sys
sys.stdout.reconfigure(encoding='utf-8')

class content_praser:
    def respond(self, target_input):
        provider = GoogleProvider(api_key='AIzaSyCJhwbGTw10OIe7Lyo1VMSVZu7ts13iHro')
        model = GoogleModel('gemini-1.5-flash', provider=provider)
        agent = Agent(model, system_prompt = 'Please break down the concepts of the input smartly and pack them into a JSON format. Please keep your answer concised and the pointers precised. Make sure, as you break it down the details of the company mentioned in the article should be mentioned first')
        result = agent.run_sync(f""" 
                        {target_input}
                        """)
        result = result.output  
        return result
    
''' This is a content praser. It can take input as the conetnts in the article. Then the article is parsed and then JSON output is generated in order to store the insights from the article.
Note it needs the JSON extracter code to change the string into JSON'''