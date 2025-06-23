import streamlit as st
import json
from bot.chatbot import Interact
from bot.logger import log_interaction
from bot.session_memory import SessionMemory
import os

# Agents + dependencies
from dependencies import input_manager, JSON_extractor
from agents.content_praser import content_praser
from agents.senti_analyser import sent_analysis
from agents.insight import insi_analysis

# Instantiate models
input_parse = input_manager.input_manager()
json_extractor = JSON_extractor.extract_json()
content_praser = content_praser()
sentiment_agent = sent_analysis()
insights = insi_analysis()

# API + chatbot memory
API_KEY = 'AIzaSyCJhwbGTw10OIe7Lyo1VMSVZu7ts13iHro'
bot = Interact(api_key=API_KEY)
session = SessionMemory(max_memory=5)

# Internal state for analysis
if 'article_context' not in st.session_state:
    st.session_state['article_context'] = ""

# Streamlit UI
st.title("Your friednly financial analyst")

uploaded_file = st.file_uploader("Upload a .json file (financial article)", type=["json"])
user_input = st.text_area("Ask something about the article or general")

if uploaded_file:
    file_content = uploaded_file.read()
    try:
        temp_json_path = "temp_uploaded.json"
        with open(temp_json_path, 'wb') as f:
            f.write(file_content)

        article_id, headline, content, timestamp = input_parse.load_json_as_dict(temp_json_path)

        if st.button("Analyze Uploaded Article"):
            with st.spinner("Analyzing..."):
                sent_output = sentiment_agent.respond(content)
                insights_out = insights.respond(sent_output)

                insights_out = insights_out[7:-4]
                try:
                    insights_json = json.loads(insights_out)
                    st.success("🧠 Analysis Complete")
                    st.json(insights_json)

                    # Store as structured article context
                    article_context = f"""Article Headline: {headline}
Date: {timestamp}

Content:
{content}

Sentiment Analysis:
{sent_output}

Extracted Insights:
{json.dumps(insights_json, indent=2)}
"""
                    st.session_state['article_context'] = article_context

                except json.JSONDecodeError:
                    st.error("Could not parse insights into JSON.")
    except Exception as e:
        st.error(f"Error parsing file: {e}")

# Chat interaction
if st.button("Send"):
    combined_context = session.get_context()
    full_context = st.session_state['article_context'] + "\n\n" + combined_context

    response = bot.respond(user_input, context=full_context)
    session.add(user_input, response)
    log_interaction(user_input, response)
    st.markdown(f"**Bot:** {response}")

# Memory display
if st.checkbox("Show Session Memory"):
    st.text(session.get_context())
