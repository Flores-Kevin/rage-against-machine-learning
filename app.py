import streamlit as st
from streamlit_option_menu import option_menu
import streamlit.components.v1 as html
from pprint import pprint
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, MinMaxScaler, Normalizer
from sklearn.metrics.pairwise import cosine_similarity

#import spotify keys
from config import client_id
from config import client_secret
from recommend_tracks import createToken, searchTrack, recommendSongs

st.set_page_config(layout="wide")

regions = ['Argentina', 'Australia', 'Austria', 'Belarus', 'Belgium', 'Bolivia', 'Brazil', 'Bulgaria', 'Canada', 'Chile', 'Colombia', 'Costa Rica', 'Cyprus', 'Czech Republic', 'Denmark', 'Dominican Republic', 'Ecuador', 'Egypt', 'El Salvador', 'Estonia', 'Finland', 'France', 'Germany', 'Global', 'Greece', 'Guatemala', 'Honduras', 'Hong Kong', 'Hungary', 'Indonesia', 'Ireland', 'Israel', 'Italy', 'Japan', 'Kazakhstan', 'Latvia', 'Lithuania', 'Luxembourg', 'Malaysia', 'Mexico', 'Netherlands', 'New Zealand', 'Nicaragua', 'Nigeria', 'Norway', 'Pakistan', 'Panama', 'Paraguay', 'Peru', 'Philippines', 'Poland', 'Portugal', 'Romania', 'Saudi Arabia', 'Singapore', 'Slovakia', 'South Africa', 'South Korea', 'Spain', 'Sweden', 'Switzerland', 'Taiwan', 'Thailand', 'Turkey', 'UAE', 'Ukraine', 'United Kingdom', 'Uruguay', 'Venezuela', 'Vietnam']


with st.sidebar:
    choose = option_menu("Select Page", ['Home','Music Diversifier'],
                         icons=['house', 'music-player-fill'],
                         menu_icon="app-indicator", default_index=0,
                         styles={
        "container": {"padding": "5!important", "background-color": "#white"},
        "icon": {"color": "black", "font-size": "25px"}, 
        "nav-link": {"font-size": "16px", "text-align": "left", "margin":"0px", "--hover-color": "#eee"},
        "nav-link-selected": {"background-color": "#02ab21"},
    }
    )

# app_mode = st.sidebar.selectbox('Select Page',['Home','Music Diversifier'])

if choose=='Home':
    st.title('Rage Against The Machine Learning')
    st.markdown('## Welcome to our app!')
    # df=pd.read_csv('emp_analytics.csv')
    # st.write(df.head())
    st.write("We've created a Music Diversifier to help expand your musical horizons. Once you input a favorite song of yours and select a region you're interested in, our app will return the five most similar songs from that region's Top 200 Chart.")
    st.write("Please note: our app is currently only working with chart data from the week of 9/30/22 - 10/6/22.")


if choose=='Music Diversifier':
    st.title('Music Diversifier')
    st.markdown('Please enter information about a song you like:')
    
    with st.form(key='my_form'):
        track = st.text_input('Song name:')
        artist = st.text_input('Artist name:')
        # st.markdown('Regional Top 200 Chart:')
        region = st.selectbox('Regional Top 200 Chart:', regions)
    
        clicked = st.form_submit_button("Find Songs")
        
        st.markdown('---')

        if clicked:
            results = recommendSongs(track, artist, region)

            st.write(results.iloc[:,1:4])

            results_info = results.drop(columns=['Similarity Score'])
            # st.write(results_info)
            input_info = searchTrack(track,artist)
            input_info = input_info.rename(columns = {'track_id':'Track ID', 
            'track_name':'Track Name', 
            'artist_names':'Artist Name(s)', 
            'danceability':'Danceability',
            'energy':'Energy',
            'loudness':'Loudness',
            'mode':'Mode',
            'speechiness':'Speechiness',
            'acousticness':'Acousticness',
            'instrumentalness':'Instrumentalness',
            'liveness':'Liveness',
            'valence':'Valence',
            'tempo':'Tempo'})

            combined_df = pd.concat([input_info,results_info.loc[:]]).reset_index(drop=True)    
            st.write(combined_df.iloc[:,1:13])

