import json
from datetime import datetime

LOG_FILE = 'interaction_log.json'

def log_interaction(user_input, bot_response):
    entry = {
        'timestamp': datetime.now().isoformat(),
        'user_input': user_input,
        'bot_response': bot_response
    }
    with open(LOG_FILE, 'a', encoding='utf-8') as f:
        f.write(json.dumps(entry) + '\n')
