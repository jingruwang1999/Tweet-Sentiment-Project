import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import matplotlib.pyplot as plt
import wordcloud

st.title("Sentiment Analysis of Tweets on US Airlines")
st.sidebar.title("Sentiment Analysis of Tweets on US Airlines")

st.markdown("This app is a Streamlit dashboard to analyze the sentiment of Tweets")
st.sidebar.markdown("This app is a Streamlit dashboard to analyze the sentiment of Tweets 🐦")

DATA_URL = "~/Desktop/Tweets.csv"
@st.cache(persist=True)
def load_data():
    data = pd.read_csv(DATA_URL)
    data["tweet_created"] = pd.to_datetime(data["tweet_created"])
    return data

data = load_data()
st.write(data)

st.sidebar.subheader("Show Random Tweet")
random_tweet = st.sidebar.radio('Sentiment', ('positive', 'neutral', 'negative'))
tweet = data[data['airline_sentiment'] == random_tweet][["text"]].sample(n=1).iat[0,0]
st.sidebar.markdown(tweet)

st.sidebar.markdown("### Number of tweets by sentiment")
select = st.sidebar.selectbox("Visualization Type", ["Histogram", "Pie Chart"], key = "1")
sentiment_count = data["airline_sentiment"].value_counts()
sentiment_count = pd.DataFrame({"Sentiment":sentiment_count.index, 'Tweets':sentiment_count.values})

if not st.sidebar.checkbox("Hide", True):
    st.markdown("### Number of Tweets by Sentiment")
    if select == "Histogram":
        fig = px.bar(sentiment_count, x = "Sentiment", y = "Tweets", color = "Tweets", height = 500)
        st.plotly_chart(fig)
    else:
        fig = px.pie(sentiment_count, values="Tweets", names = "Sentiment")
        st.plotly_chart(fig)

st.sidebar.subheader("Time and Location of tweet")
hour = st.sidebar.slider("Hour of day", 0, 23)
modified_data = data[data["tweet_created"].dt.hour == hour]
if not st.sidebar.checkbox("Close", True, key = '1'):
    st.markdown("### Tweets locations based on the time of day")
    st.markdown("%i tweets between %i:00 and %i:00" % (len(modified_data), hour, (hour+1)%24))
    st.map(modified_data)

st.sidebar.subheader("Breakdown airline tweets by sentiment")
choice = st.sidebar.multiselect("Pick airlines", ("US Airways", "United", "American", "Virgin America"), key='0')

if len(choice) > 0:
    choice_data = data[data.airline.isin(choice)]
    fig_choice = px.histogram(choice_data, x='airline', y='airline_sentiment', histfunc='count', color='airline',
    facet_col = 'airline_sentiment', labels={'airline_sentiment':'tweets'}, height=600, width=800)
    st.plotly_chart(fig_choice)
