from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from textblob import TextBlob
from transformers import pipeline
import pandas as pd

class UnifiedSentimentAnalyzer:
    def __init__(self):
        self.vader_analyzer = SentimentIntensityAnalyzer()
        self.transformers_pipeline = pipeline(
            "sentiment-analysis",
            model="distilbert-base-uncased-finetuned-sst-2-english"
        )
    
    def analyze_text(self, text):
        # VADER Analysis
        vader_scores = self.vader_analyzer.polarity_scores(text)
        
        # TextBlob Analysis
        blob = TextBlob(text)
        textblob_polarity = blob.sentiment.polarity
        textblob_subjectivity = blob.sentiment.subjectivity
        
        # Transformers Analysis
        try:
            transformers_result = self.transformers_pipeline(text[:512])[0]  # Limit length
            transformers_label = transformers_result['label']
            transformers_score = transformers_result['score']
        except:
            transformers_label = "NEUTRAL"
            transformers_score = 0.5
        
        # Unified Score (Custom weighted average)
        unified_score = self.calculate_unified_score(
            vader_scores['compound'], 
            textblob_polarity, 
            transformers_score, 
            transformers_label
        )
        
        return {
            'text': text,
            'vader': {
                'compound': vader_scores['compound'],
                'positive': vader_scores['pos'],
                'negative': vader_scores['neg'],
                'neutral': vader_scores['neu']
            },
            'textblob': {
                'polarity': textblob_polarity,
                'subjectivity': textblob_subjectivity
            },
            'transformers': {
                'label': transformers_label,
                'score': transformers_score
            },
            'unified_score': unified_score,
            'unified_sentiment': self.score_to_sentiment(unified_score)
        }
    
    def calculate_unified_score(self, vader_compound, textblob_polarity, transformers_score, transformers_label):
        # Convert transformers label to numeric
        transformers_numeric = transformers_score if transformers_label == "POSITIVE" else -transformers_score
        
        # Weighted average (adjust weights based on your preference)
        weights = {'vader': 0.4, 'textblob': 0.3, 'transformers': 0.3}
        
        unified = (vader_compound * weights['vader'] + 
                  textblob_polarity * weights['textblob'] + 
                  transformers_numeric * weights['transformers'])
        
        return unified
    
    def score_to_sentiment(self, score):
        if score >= 0.05:
            return "POSITIVE"
        elif score <= -0.05:
            return "NEGATIVE"
        else:
            return "NEUTRAL"
    
    def analyze_batch(self, texts):
        return [self.analyze_text(text) for text in texts]