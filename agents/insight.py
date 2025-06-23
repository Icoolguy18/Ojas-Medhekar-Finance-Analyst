from pydantic_ai import Agent
from pydantic_ai.models.google import GoogleModel
from pydantic_ai.providers.google import GoogleProvider

import sys
sys.stdout.reconfigure(encoding='utf-8')

class insi_analysis:
    def respond(self, gen_cont):
        provider = GoogleProvider(api_key='AIzaSyCJhwbGTw10OIe7Lyo1VMSVZu7ts13iHro')
        model = GoogleModel('gemini-1.5-flash', provider=provider)
        agent = Agent(model, system_prompt = '''
You are a highly specialized Financial Sentiment Analysis AI. Your primary task is to meticulously analyze the provided financial sentiment analysis score and generate insights on those. Please note you also have to score out on the basis of the provided sentiment value. the output should be in format 
{
    "insights": generated_insight_values,
    "score": final_score_on_understanding_and_insights
  }

                    ''')
        result = agent.run_sync(f""" 
                        {gen_cont}
                        """)
        result = result.output  
        return result
    
