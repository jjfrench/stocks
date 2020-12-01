from nltk.sentiment.vader import SentimentIntensityAnalyzer

def SentimentAnalyzer(text):
    sentiment = SentimentIntensityAnalyzer(text)
    return sentiment
