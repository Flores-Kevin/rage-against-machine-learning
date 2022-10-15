import streamlit as st
import requests
import json
from pprint import pprint
import pandas as pd
import time
import numpy as np
from sklearn.preprocessing import StandardScaler, MinMaxScaler, Normalizer
from sklearn.metrics.pairwise import cosine_similarity

#import spotify keys
from config import client_id
from config import client_secret
from recommend_tracks import createToken, searchTrack, recommendSongs

regions = ['Argentina', 'Australia', 'Austria', 'Belarus', 'Belgium', 'Bolivia', 'Brazil', 'Bulgaria', 'Canada', 'Chile', 'Colombia', 'Costa Rica', 'Cyprus', 'Czech Republic', 'Denmark', 'Dominican Republic', 'Ecuador', 'Egypt', 'El Salvador', 'Estonia', 'Finland', 'France', 'Germany', 'Global', 'Greece', 'Guatemala', 'Honduras', 'Hong Kong', 'Hungary', 'Indonesia', 'Ireland', 'Israel', 'Italy', 'Japan', 'Kazakhstan', 'Latvia', 'Lithuania', 'Luxembourg', 'Malaysia', 'Mexico', 'Netherlands', 'New Zealand', 'Nicaragua', 'Nigeria', 'Norway', 'Pakistan', 'Panama', 'Paraguay', 'Peru', 'Philippines', 'Poland', 'Portugal', 'Romania', 'Saudi Arabia', 'Singapore', 'Slovakia', 'South Africa', 'South Korea', 'Spain', 'Sweden', 'Switzerland', 'Taiwan', 'Thailand', 'Turkey', 'UAE', 'Ukraine', 'United Kingdom', 'Uruguay', 'Venezuela', 'Vietnam']

app_mode = st.sidebar.selectbox('Select Page',['Rage Against The Machine Learning','Music Diversifier'])

if app_mode=='Home':
    st.title('Home')
    st.markdown('Dataset:')
    # df=pd.read_csv('emp_analytics.csv')
    # st.write(df.head())
    st.write('testing')


if app_mode=='Music Diversifier':
    st.title('Music Diversifier')
    st.markdown('Please type a song from Spotify :')
    track = st.text_input('Song name')
    artist = st.text_input('Artist name')

    st.markdown('Please select a region :')
    region = st.selectbox('Pick One', regions)
    st.button("Find Songs")
 
    results = recommendSongs(track, artist, region)
    st.dataframe(results.iloc[:,1:4])
    
    
    
