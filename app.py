import streamlit as st
from streamlit_option_menu import option_menu
import streamlit.components.v1 as components
from  PIL import Image
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
    choose = option_menu(None, ['Home','Music Diversifier', 'Our Team'],
                         icons=['house', 'music-player-fill', 'people-fill'],
                         menu_icon="app-indicator", default_index=0,
                         styles={
        "container": {"padding": "5!important", "background-color": "#white"},
        "icon": {"color": "black", "font-size": "25px"}, 
        "nav-link": {"font-size": "16px", "text-align": "left", "margin":"0px", "--hover-color": "#eee"},
        "nav-link-selected": {"background-color": "#02ab21"},
    }
    )


if choose=='Home':
    st.title('Rage Against The Machine Learning')
    st.markdown('## Welcome to our app!')
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
        # clicked = st.button("Find Songs", on_click=callback)


    if clicked:
        results = recommendSongs(track, artist, region)

        st.markdown(""" ### Results: """)
        st.write(results.iloc[:,1:4])

        st.markdown(""" ### Compare Track Audio Features: """)
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

        st.markdown(""" ### Preview Recommended Songs: """)
        for t in range(len(results)):
            track_id = results.iloc[t,0]
            embed = f'<iframe style="border-radius:0px" src="https://open.spotify.com/embed/track/{track_id}?utm_source=generator&theme=0" width="50%" height="80" frameBorder="0" allowfullscreen="" allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture"></iframe>'
            st.write(f'Recommendation {t+1}:')
            components.html(embed)



# github_logo = Image.open('assets/img/team/GitHub-Mark-120px-plus.png')
# linkedin_logo = Image.open('assets/img/team/LI-In-Bug.png')
dan_profile = Image.open('assets/img/team/dan.jpeg')
kevin_profile = Image.open('assets/img/team/kevin.jpeg')
molly_profile = Image.open('assets/img/team/molly.jpeg')
slone_profile = Image.open('assets/img/team/slone.jpeg')

    
if choose=='Our Team':
    st.title('Our Team')
    col1, col2 = st.columns( [0.5, 0.5])

    with col1: 
        st.markdown('## Dan')
        st.image(dan_profile, width=150 )
        st.markdown("insert blurb here")
        st.markdown("""[GitHub](https://github.com/dtmurphy6)    
        [LinkedIn](https://www.linkedin.com/in/danielmurphy3/)""")

        st.markdown('## Molly')
        st.image(molly_profile, width=150 )
        st.markdown("insert blurb here")
        st.markdown("""[GitHub](https://github.com/mbruns13)    
        [LinkedIn](https://www.linkedin.com/in/mollybruns)""")


    with col2: 
        st.markdown('## Kevin')
        st.image(kevin_profile, width=150 )
        st.markdown("insert blurb here")
    # st.markdown("""<a href="https://github.com/flores-kevin"><i class="bi bi-github"></i></a>
        #                                         <a href="https://www.linkedin.com/in/kevin-flores-097991237/"><i class="bi bi-linkedin"></i></a>
        # """)
        st.markdown("""[GitHub](https://github.com/flores-kevin)    
        [LinkedIn](https://www.linkedin.com/in/kevin-flores-097991237)""")

        st.markdown('## Slone')
        st.image(slone_profile, width=150 )
        st.markdown("insert blurb here")
        st.markdown("""[GitHub](https://github.com/bslone1)    
        [LinkedIn](https://www.linkedin.com/in/bridget-slone-021bs/)""")

