from pydantic_ai import Agent
from pydantic_ai.models.google import GoogleModel
from pydantic_ai.providers.google import GoogleProvider

class Interact:
    def __init__(self, api_key: str, system_prompt: str = ''):
        provider = GoogleProvider(api_key=api_key)
        model = GoogleModel('gemini-1.5-flash', provider=provider)
        self.agent = Agent(model, system_prompt=system_prompt)

    def respond(self, input_text: str, context: str = '') -> str:
        combined_input = f"{context}\n{input_text}" if context else input_text
        result = self.agent.run_sync(combined_input)
        return result.output
