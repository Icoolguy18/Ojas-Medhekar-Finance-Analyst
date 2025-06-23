# AI-Powered Financial Chatbot and Article Analysis System

This project combines a conversational AI chatbot with a modular system for processing financial articles, extracting key information, performing sentiment analysis, and generating insightful summaries. It leverages Google's Gemini-1.5-Flash model through the `pydantic-ai` library for its conversational and analytical capabilities, complemented by robust logging and session memory management.

## Table of Contents

-   [Project Overview](#project-overview)
-   [System Architecture: Why Multiple Agents?](#system-architecture-why-multiple-agents)
-   [Core Components](#core-components)
-   [Data Models](#data-models)
-   [Getting Started](#getting-started)
-   [Usage](#usage)
-   [Dependencies](#dependencies)

## Project Overview

The "AI-Powered Financial Chatbot and Article Analysis System" is designed to offer a multifaceted solution:
1.  **Interactive Chatbot:** Engages users in a conversation, capable of responding to queries and potentially acting as an interface for the analysis tools.
2.  **Financial Article Processing:** Automates the understanding of financial news by parsing raw article content, analyzing sentiment towards specific entities, and synthesizing these findings into actionable insights.
3.  **Logging and Context Management:** Ensures that interactions are recorded and short-term conversational context is maintained for a smoother user experience.

## System Architecture: Why Multiple Agents?

The system employs a multi-agent or modular architecture, with distinct Python files acting as specialized "agents" or modules. This design provides several benefits, crucial for both conversational AI and complex data processing:

* **Separation of Concerns:** Each agent has a distinct, focused responsibility, making the codebase cleaner, more manageable, and easier to debug. For instance, conversational logic is separate from article parsing.
* **Modularity & Reusability:** Individual agents can be developed, tested, and potentially reused independently. The `content_praser` could be used alone, or the `senti_analyser` integrated into a different application.
* **Orchestration of Complex Workflow:** Both chatbot interactions and financial analysis involve multiple sequential or parallel steps. Breaking these into separate agents allows for a clear, pipeline-like flow of data and control.
* **Specialized Prompts/Logic:** Each AI-powered agent can be given a highly specific system prompt tailored to its exact task (e.g., parsing vs. sentiment analysis), maximizing the effectiveness of the underlying AI model for that particular step. Similarly, utility agents like `logger` and `session_memory` have their own focused logic.

## Core Components

The project consists of the following key Python modules, each representing a specialized agent or utility:

1.  ### `chatbot.py`
    * **Role:** This module defines the `Interact` class, which serves as the primary conversational agent. It handles user input, generates bot responses using the Gemini-1.5-Flash model, and can incorporate conversational context for more coherent dialogue.
    * **Purpose Rationale:** Provides the core conversational interface of the system, acting as the front-end for user interaction and potentially orchestrating calls to other analysis agents based on user queries.

2.  ### `session_memory.py`
    * **Role:** This module implements the `SessionMemory` class, designed to store a capped number of recent user-bot interaction pairs. It uses a `deque` (double-ended queue) to manage memory, ensuring that only the most recent interactions are retained for context.
    * **Purpose Rationale:** Crucial for maintaining short-term conversational context, allowing the chatbot to remember previous turns and respond more naturally and relevantly within a given session. This directly addresses the challenge of context persistence in AI conversations.

3.  ### `logger.py`
    * **Role:** This module provides the `log_interaction` function, which is responsible for recording all user inputs and bot responses to a JSON file named `interaction_log.json`. Each entry includes a timestamp for auditing.
    * **Purpose Rationale:** Essential for debugging, monitoring chatbot performance, analyzing user interaction patterns, and potentially gathering data for future model training or refinement. Provides an auditable trail of conversations.

4.  ### `content_praser.py`
    * **Role:** This module contains the `content_praser` class. Its primary function is to take raw article content as input. It then intelligently breaks down the concepts within the article and formats them into a concise JSON output, prioritizing details about companies mentioned.
    * **Purpose Rationale:** Acts as the initial data structuring layer for financial articles, converting unstructured text into a machine-readable, organized format for subsequent analytical processing.

5.  ### `senti_analyser.py`
    * **Role:** This module houses the `sent_analysis` class. It acts as a specialized Financial Sentiment Analysis AI, meticulously analyzing financial article content to determine sentiment (positive, negative, or neutral) for specific entities. It also assigns a numerical sentiment score and provides concise reasoning in a structured JSON array format.
    * **Purpose Rationale:** Provides granular sentiment scores for individual entities, which is crucial for detailed financial insights beyond overall article sentiment.

6.  ### `insight.py`
    * **Role:** This module defines the `insi_analysis` class. It is a highly specialized Financial Sentiment Analysis AI that analyzes a given financial sentiment analysis score. Its task is to generate insights based on these scores and provide an overall score reflecting its understanding and the quality of the insights.
    * **Purpose Rationale:** Converts raw sentiment scores into meaningful, human-understandable financial insights, effectively summarizing the implications of the sentiment analysis.

## Data Models

The `models.py` file defines the data structures (using `pydantic.BaseModel`) used throughout the application to ensure data consistency and validation:

* **`Article`**: Represents an article with `title`, `body`, and optional `published_date` and `source`.
* **`Entity`**: Represents an identified entity with a `name` and `confidence` score.
* **`Sentiment`**: Captures the `entity_name`, `sentiment` (positive, negative, neutral), `score` (float between 0.0 and 1.0), and `reasoning`.
* **`TickerMapping`**: Maps an `entity_name` to a stock `ticker` and optional `exchange`.

## Getting Started

To get this project up and running, you'll need Python installed and the necessary libraries.

### Prerequisites

* Python 3.x
* A Google Cloud project with access to the Gemini API (as indicated by the `api_key` in the code).

### Installation

1.  Clone the repository:
    ```bash
    git clone [https://github.com/Icoolguy18/Ojas-Medhekar-Finance-Analyst.git](https://github.com/Icoolguy18/Ojas-Medhekar-Finance-Analyst.git)
    cd Ojas-Medhekar-Finance-Analyst
    ```
2.  Install the required Python packages. Based on the imports, `pydantic-ai` and `pydantic` are crucial.
    ```bash
    pip install pydantic pydantic-ai
    ```
    *Note: Ensure your `API_KEY` for `GoogleProvider` is correctly set up in `content_praser.py`, `senti_analyser.py`, `insight.py`, and `chatbot.py`. The provided example `AIzaSyCJhwbGTw10OIe7Lyo1VMSVZu7ts13iHro` is a placeholder and should be replaced with your actual API key for functionality.*

## Usage

The project's components are designed to work together, forming a conversational and analytical pipeline.

### Core Chatbot Interaction

You can use the `chatbot.py` module to instantiate a conversational agent:

```python
from chatbot import Interact
from session_memory import SessionMemory
from logger import log_interaction

# Initialize memory and chatbot
session_memory = SessionMemory(max_memory=5) # Keeps last 5 turns
chat_bot = Interact(api_key='YOUR_ACTUAL_API_KEY', system_prompt='You are a helpful financial assistant.')

def run_chat_session():
    print("Chatbot initialized. Type 'exit' to end.")
    while True:
        user_input = input("User: ")
        if user_input.lower() == 'exit':
            break

        # Get current context from memory
        context = session_memory.get_context()

        # Get bot response
        bot_response = chat_bot.respond(user_input, context=context)

        # Log and add to memory
        log_interaction(user_input, bot_response)
        session_memory.add(user_input, bot_response)

        print(f"Bot: {bot_response}")

# To start the session:
if __name__ == "__main__":
    run_chat_session()
