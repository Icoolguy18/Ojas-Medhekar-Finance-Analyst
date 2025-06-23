# Financial Article Analysis and Insights Generator

This project provides a modular system for processing financial articles, extracting key information, performing sentiment analysis, and generating insightful summaries. It leverages Google's Gemini-1.5-Flash model through the `pydantic-ai` library to achieve its analytical capabilities.

## Table of Contents

-   [Project Overview](#project-overview)
-   [System Architecture: Why Multiple Agents?](#system-architecture-why-multiple-agents)
-   [Core Components](#core-components)
-   [Data Models](#data-models)
-   [Getting Started](#getting-started)
-   [Usage](#usage)
-   [Dependencies](#dependencies)

## Project Overview

The "Financial Article Analysis and Insights Generator" is designed to automate the process of understanding financial news. It takes raw article content, parses it into a structured format, analyzes the sentiment towards specific entities mentioned, and then synthesizes these findings into actionable insights.

## System Architecture: Why Multiple Agents?

The system employs a multi-agent architecture, with each Python file essentially acting as a specialized "agent" or module. This design provides several benefits:

* **Separation of Concerns:** Each agent has a distinct, focused responsibility, making the codebase cleaner, more manageable, and easier to debug.
* **Modularity & Reusability:** Individual agents can be developed, tested, and potentially reused independently. For example, the `senti_analyser` could be used in a different project requiring only sentiment analysis.
* **Orchestration of Complex Workflow:** Financial analysis involves multiple sequential steps (parsing, sentiment, insights). Breaking these into separate agents allows for a clear, pipeline-like flow of data through different specialized processing stages.
* **Specialized Prompts:** Each agent can be given a highly specific system prompt tailored to its exact task, maximizing the effectiveness of the underlying AI model for that particular step.

## Core Components

The project consists of the following key Python modules, each representing a specialized agent:

1.  ### `content_praser.py`
    * **Role:** This module contains the `content_praser` class. Its primary function is to take raw article content as input. It then intelligently breaks down the concepts within the article and formats them into a concise JSON output. The system prompt emphasizes prioritizing details about companies mentioned in the article.
    * **Purpose Rationale:** Acts as the initial data structuring layer, converting unstructured text into a machine-readable, organized format for subsequent processing.

2.  ### `senti_analyser.py`
    * **Role:** This module houses the `sent_analysis` class. It acts as a specialized Financial Sentiment Analysis AI. Its task is to meticulously analyze provided financial article content to determine the sentiment (positive, negative, or neutral) for specific entities. It also assigns a numerical sentiment score and provides concise reasoning in a structured JSON array format.
    * **Purpose Rationale:** Provides granular sentiment scores for individual entities, which is crucial for detailed financial insights beyond overall article sentiment.

3.  ### `insight.py`
    * **Role:** This module defines the `insi_analysis` class. It is a highly specialized Financial Sentiment Analysis AI that analyzes a given financial sentiment analysis score. Its task is to generate insights based on these scores and provide an overall score reflecting its understanding and the quality of the insights, in a JSON format containing "insights" and "score" keys.
    * **Purpose Rationale:** Converts raw sentiment scores into meaningful, human-understandable insights, effectively summarizing the implications of the sentiment analysis.

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
2.  Install the required Python packages. Based on the imports, `pydantic-ai` is crucial. You might also need `pydantic`.
    ```bash
    pip install pydantic pydantic-ai
    ```
    *Note: Ensure your `API_KEY` for GoogleProvider is correctly set up in `content_praser.py`, `senti_analyser.py`, and `insight.py`. The provided example `AIzaSyCJhwbGTw10OIe7Lyo1VMSVZu7ts13iHro` is a placeholder and should be replaced with your actual API key for functionality.*

## Usage

The project is designed as a pipeline. Here's a high-level conceptual flow based on the agents:

1.  **Input Article Content:** Provide the financial article text as input to the `content_praser` class.
    ```python
    from content_praser import content_praser
    article_text = "Your financial article content here..."
    parsed_json_output = content_praser().respond(article_text)
    # This parsed_json_output then needs to be converted from string to JSON object if it's a string.
    ```
2.  **Perform Sentiment Analysis:** Take the relevant parts of the parsed content (e.g., the article body or specific entity mentions) and feed it to the `senti_analyser`.
    ```python
    from senti_analyser import sent_analysis
    # Assuming 'parsed_json_output' contains the article body
    sentiment_analysis_results = sent_analysis().respond(parsed_json_output)
    ```
3.  **Generate Insights:** Use the sentiment analysis results as input for the `insight` module to generate a summary and score.
    ```python
    from insight import insi_analysis
    insights_and_score = insi_analysis().respond(sentiment_analysis_results)
    ```

*Note: The exact orchestration logic to chain these steps together (e.g., in a `main.py` file or a workflow script) is not provided in the current files, but this represents the logical flow.*

## Dependencies

* `pydantic-ai`: Used for integrating with AI models (specifically Google's Gemini-1.5-Flash) and handling structured outputs.
* `pydantic`: Used for defining data models and ensuring data validation and serialization.
