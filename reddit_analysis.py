import pandas as pd
from collections import Counter
from textblob import TextBlob
import re

def analyze_sentiment_and_keywords(input_csv, subreddit):
   
    df = pd.read_csv(input_csv)

    # Combine 'title' and 'selftext' into a single column for analysis
    combined_text = (df['title'].fillna('') + ' ' + df['selftext'].fillna('')).dropna()

    # Clean the data by making lowercase and removing non-a to z characters
    combined_text = combined_text.str.lower().apply(lambda x: re.sub(r'[^a-z\s]', ' ', x))
    
    word_counter = Counter()

    
    for text in combined_text:
        words = text.split()  
        word_counter.update(words)  

    
    top_100_keywords = pd.DataFrame(word_counter.most_common(100), columns=['keyword', 'frequency'])

    
    # Print out keyword counts
    for index, row in top_100_keywords.iterrows():
        print(f"{row['keyword']}: {row['frequency']}")

    # Categorize each as positive, negative, or neutral
    def categorize_sentiment(text):
        polarity = TextBlob(text).sentiment.polarity
        if polarity > 0:
            return 'Positive'
        elif polarity < 0:
            return 'Negative'
        else:
            return 'Neutral'

    
    sentiment_categories = combined_text.apply(categorize_sentiment)

    
    sentiment_results = pd.DataFrame({'combined_text': combined_text, 'sentiment': sentiment_categories})

    
    print("\nSentiment Analysis Results:")
    for index, row in sentiment_results.iterrows():
        print(f"Combined Text: {row['combined_text'][:50]}... | Sentiment: {row['sentiment']}")

    # Count the sentiment categories
    sentiment_counts = sentiment_results['sentiment'].value_counts()

    
    
    print("Positive:", sentiment_counts.get('Positive', 0))
    print("Negative:", sentiment_counts.get('Negative', 0))
    print("Neutral:", sentiment_counts.get('Neutral', 0))

    
    keywords_output_csv = f"{subreddit}_subreddit_top_100_keywords.csv"
    sentiment_output_csv = f"{subreddit}_subreddit_sentiment_analysis_results.csv"
    top_100_keywords.to_csv(keywords_output_csv, index=False)
    sentiment_results.to_csv(sentiment_output_csv, index=False)

analyze_sentiment_and_keywords(
    input_csv='INSERT YOUR PATH',
    subreddit='ComputerSecurity'
)

analyze_sentiment_and_keywords(
    input_csv='INSERT YOUR PATH',
    subreddit='DigitalPrivacy'
)
