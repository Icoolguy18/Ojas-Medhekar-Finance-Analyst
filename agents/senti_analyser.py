from pydantic_ai import Agent
from pydantic_ai.models.google import GoogleModel
from pydantic_ai.providers.google import GoogleProvider

import sys
sys.stdout.reconfigure(encoding='utf-8')

class sent_analysis:
    def respond(self, cont):
        provider = GoogleProvider(api_key='AIzaSyCJhwbGTw10OIe7Lyo1VMSVZu7ts13iHro')
        model = GoogleModel('gemini-1.5-flash', provider=provider)
        agent = Agent(model, system_prompt = '''You are a highly specialized Financial Sentiment Analysis AI. Your primary task is to meticulously analyze the provided financial article content and determine the sentiment (positive, negative, or neutral) for specific entities mentioned within it. You must also assign a numerical sentiment score and provide a concise reasoning.

**Input:**
the inpput will be seperated content format for the article, consisting of the article body
please give the output in the format
[
  {
    "entity_name": "string",
    "sentiment": "positive" | "negative" | "neutral",
    "score": "float (between 0.0 and 1.0, inclusive)",
    "reasoning": "string"
  }
]
}''')
        result = agent.run_sync(f""" 
                        {cont}
                        """)
        result = result.output  
        return result
    
