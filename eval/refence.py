import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer


analyzer = SentimentIntensityAnalyzer()

text1 = "This product is amazing! Highly recommended."
text2 = "I'm not happy with the quality of this item."

# Analyze sentiment
vs1 = analyzer.polarity_scores(text1)
vs2 = analyzer.polarity_scores(text2)

print(f"Text 1: {vs1}")
print(f"Text 2: {vs2}")
# The 'compound' score is a normalized, weighted composite score ranging from -1 (most extreme negative) to +1 (most extreme positive).