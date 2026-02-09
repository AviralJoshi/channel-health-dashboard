import streamlit as st
import pandas as pd
import os

st.title("Basic Streamlit CSV Viewer")

# Define the path to the CSV file
csv_file_path = "data/youtube_data.csv"

# Check if the file exists
if os.path.exists(csv_file_path):
    try:
        # Load the CSV file
        df = pd.read_csv(csv_file_path)
        
        # Calculate Engagement Rate
        df['Engagement Rate'] = (df['Likes'] + df['Comments']) / df['Views']
        
        # Display Key Metrics
        st.subheader("Key Metrics")
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Views", f"{df['Views'].sum():,}")
        col2.metric("Total Likes", f"{df['Likes'].sum():,}")
        col3.metric("Avg Engagement Rate", f"{df['Engagement Rate'].mean():.2%}")
        
        st.write("### Column Names:")
        st.write(list(df.columns))
        
        st.write("### Data with Engagement Rate:")
        # Display the first 5 rows with the new column, formatted
        st.dataframe(df.head(5).style.format({"Engagement Rate": "{:.2%}"}))
        
        st.write("### Full Data (Optional):")
        if st.checkbox("Show full dataset"):
            st.dataframe(df.style.format({"Engagement Rate": "{:.2%}"}))
            
        # Sentiment Analysis Section
        st.subheader("Comment Sentiment Analyzer")
        comments_file = "data/comments.csv"
        
        if os.path.exists(comments_file):
            try:
                from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
                analyzer = SentimentIntensityAnalyzer()
                
                # Load comments (no header)
                comments_df = pd.read_csv(comments_file, header=None, names=['Comment'])
                
                # Function to get sentiment
                def get_sentiment(text):
                    score = analyzer.polarity_scores(str(text))['compound']
                    if score > 0.05:
                        return 'Positive'
                    elif score < -0.05:
                        return 'Negative'
                    else:
                        return 'Neutral'
                
                # Apply sentiment analysis
                comments_df['Sentiment'] = comments_df['Comment'].apply(get_sentiment)
                
                # Display comments with sentiment
                st.subheader("Comments & Sentiment")
                st.dataframe(comments_df)
                
                # Show sentiment counts
                st.subheader("Sentiment Distribution")
                sentiment_counts = comments_df['Sentiment'].value_counts()
                st.bar_chart(sentiment_counts)
                
            except Exception as e:
                st.error(f"Error processing comments: {e}")
        else:
            st.warning("Comments file not found at: data/comments.csv")
            
    except Exception as e:
        st.error(f"Error loading CSV file: {e}")
else:
    st.error(f"File not found at: {csv_file_path}. Please ensure 'data/youtube_data.csv' exists.")
