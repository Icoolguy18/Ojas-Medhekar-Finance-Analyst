from collections import deque

class SessionMemory:
    def __init__(self, max_memory=5):
        self.memory = deque(maxlen=max_memory)  # capped memory

    def add(self, user_input, bot_response):
        self.memory.append((user_input, bot_response))

    def get_context(self):
        return "\n".join(f"User: {u}\nBot: {b}" for u, b in self.memory)
