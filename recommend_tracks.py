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

# create access token for spotify api
def createToken():
    #generate access token for spotify api
    #from: https://stmorse.github.io/journal/spotify-api.html

    AUTH_URL = 'https://accounts.spotify.com/api/token'

    # POST
    auth_response = requests.post(AUTH_URL, {
        'grant_type': 'client_credentials',
        'client_id': client_id,
        'client_secret': client_secret,
    })

    # convert the response to JSON
    auth_response_data = auth_response.json()

    # save the access token
    access_token = auth_response_data['access_token']

    #In order to access, we send a properly formed GET request to the API server, with our access_token in the header. Let’s save this header info now, in the following very specific format:
    headers = {
        'Authorization': 'Bearer {token}'.format(token=access_token)
    }
    
    return headers


def searchTrack(track,artist):
    #base URL for Spotify API search
    search_url = 'https://api.spotify.com/v1/search'
    
    # API search for track & artist input by user
    response = requests.get(search_url + '?q=track%3A' + track + '%20artist%3A' + artist + '&type=track%2Cartist&limit=1', headers=createToken()).json()
    
    # storing track id, artist, and track name from API search as variables
    track_id = response['tracks']['items'][0]["id"]
    artist_names = response['tracks']['items'][0]["artists"][0]['name']
    track_name = response['tracks']['items'][0]["name"]
    
    #base URL for Spotify API
    base_url = 'https://api.spotify.com/v1/'
    # API call to collect track features
    track_response = requests.get(base_url + 'audio-features/' + track_id, headers=createToken()).json()
    
    #empty lists to store song data retrieved from API call
    danceability = []
    energy = []
    # key = []
    loudness = []
    mode = []
    speechiness = []
    acousticness = []
    instrumentalness = []
    liveness = []
    valence = []
    tempo = []
    id_num = []
    # duration_mins = []
    # time_signature = []

    #fill in track info for each audio feature / empty list
    danceability.append(track_response["danceability"])
    energy.append(track_response["energy"])
    # key.append(track_response["key"])
    loudness.append(track_response["loudness"])
    mode.append(track_response["mode"])
    speechiness.append(track_response["speechiness"])
    acousticness.append(track_response["acousticness"])
    instrumentalness.append(track_response["instrumentalness"])
    liveness.append(track_response["liveness"])
    valence.append(track_response["valence"])
    tempo.append(track_response["tempo"])
    id_num.append(track_response["id"])
    # # duration recorded in api in milliseconds, converting to minutes here
    # duration_mins.append(round((track_response["duration_ms"] / 60000),2))
    # time_signature.append(track_response["time_signature"])    

    #create a dictionary to hold data gathered from the api
    track_dict = {
        "track_id": id_num,
        "artist_names": artist_names,
        "track_name": track_name,
        "danceability": danceability,
        "energy": energy,
        # "key": key,
        "loudness": loudness,
        "mode": mode,
        "speechiness": speechiness,
        "acousticness": acousticness,
        "instrumentalness": instrumentalness,
        "liveness": liveness,
        "valence": valence,
        "tempo": tempo,
        # "duration_mins": duration_mins,
        # "time_signature": time_signature,

    }
    #convert dictionary to a dataframe
    input_track_df = pd.DataFrame(track_dict)
    # input_track_df = input_track_df.drop(columns=['duration_mins'])
    return input_track_df


    
# function to recommend 5 most similar tracks from selected chart
def recommendSongs(track, artist, region):
    # run function to create DF with input track and its audio features
    user_track_df = searchTrack(track,artist)
    
    #import CSVs created in "pulling_chart_track_features.ipynb" and save as individual dfs
    features_csv_list = {"Global":"global_df.csv", "Vietnam":"vietnam_df.csv","Venezuela":"venezuela_df.csv",
    "Uruguay":"uruguay_df.csv","United Kingdom":"united_kingdom_df.csv","Ukraine":"ukraine_df.csv",
    "UAE":"uae_df.csv","Turkey":"turkey_df.csv","Thailand":"thailand_df.csv",
    "Taiwan":"taiwan_df.csv","Switzerland":"switzerland_df.csv","Sweden":"sweden_df.csv",
    "Spain":"spain_df.csv","South Korea":"south_korea_df.csv","South Africa":"south_africa_df.csv",
    "Slovakia":"slovakia_df.csv","Singapore":"singapore_df.csv","Saudi Arabia":"saudi_arabia_df.csv",
    "Romania":"romania_df.csv","Portugal":"portugal_df.csv","Poland":"poland_df.csv",
    "Philippines":"philippines_df.csv","Peru":"peru_df.csv","Paraguay":"paraguay_df.csv",
    "Panama":"panama_df.csv","Pakistan":"pakistan_df.csv","Norway":"norway_df.csv",
    "Nigeria":"nigeria_df.csv","Nicaragua":"nicaragua_df.csv","New Zealand":"new_zealand_df.csv",
    "Netherlands":"netherlands_df.csv","Mexico":"mexico_df.csv",
    "Malaysia":"malaysia_df.csv","Luxembourg":"luxembourg_df.csv","Lithuania":"lithuania_df.csv",
    "Latvia":"latvia_df.csv","Kazakhstan":"kazakhstan_df.csv","Japan":"japan_df.csv",
    "Italy":"italy_df.csv","Israel":"israel_df.csv","Ireland":"ireland_df.csv",
    "Indonesia":"indonesia_df.csv",
    "Hungary":"hungary_df.csv","Hong Kong":"hong_kong_df.csv","Honduras":"honduras_df.csv",
    "Guatemala":"guatemala_df.csv","Greece":"greece_df.csv","Germany":"germany_df.csv",
    "France":"france_df.csv","Finland":"finland_df.csv","Estonia":"estonia_df.csv",
    "El Salvador":"el_salvador_df.csv","Egypt":"egypt_df.csv","Ecuador":"ecuador_df.csv",
    "Dominican Republic":"dominican_republic_df.csv","Denmark":"denmark_df.csv","Czech Republic":"czech_republic_df.csv","Cyprus":"cyprus_df.csv","Costa Rica":"costa_rica_df.csv","Colombia":"colombia_df.csv","Chile":"chile_df.csv","Canada":"canada_df.csv","Bulgaria":"bulgaria_df.csv","Brazil":"brazil_df.csv","Bolivia":"bolivia_df.csv","Belgium":"belgium_df.csv","Belarus":"belarus_df.csv","Austria":"austria_df.csv","Australia":"australia_df.csv","Argentina":"argentina_df.csv"}
    # currently not working w/ api calls: "morocco":"morocco_df.csv","india":"india_df.csv","iceland":"iceland_df.csv"

    d = {}

    for key in features_csv_list:
        d[key] = pd.read_csv(f'resources/top_chart_features/{features_csv_list[key]}') 
        d[key] = d[key].drop(columns=['region','key','duration_mins','time_signature'])

    selected_chart_df = d[region]
    
    # create combined df of the track features from the input track and all of the tracks from the selected regional chart
    # row 0 will be the input song
    combined_df = pd.concat([user_track_df,selected_chart_df.loc[:]]).reset_index(drop=True)    
    
    # scale data (only features columns), create df of scaled data
    scaler = StandardScaler()
    # if using song_duration, needs to be combined_df.iloc[:, 3:16]
    # if using key and time_signature, needs to be combined_df.iloc[:, 3:15]
    chart_scaled = scaler.fit_transform(combined_df.iloc[:, 3:13])
    chart_scaled_df = pd.DataFrame(chart_scaled, columns=combined_df.iloc[:, 3:13].columns)

    # create array for input track data
    array1 = chart_scaled_df.iloc[0,:].to_numpy().reshape(1, -1)
    # create array for selected chart
    array2 = chart_scaled_df.iloc[1:,:].to_numpy()

    # run cosine similarity
    cosine_sim = cosine_similarity(array1, array2)
    
    # create list that is ranked by score, descending order
    sim_scores = list(enumerate(cosine_sim[-1,:]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    
    # create empty list to store recommendations
    ranked_tracks = []

    for i in range(0, 5):
        indx = sim_scores[i][0]
        ranked_tracks.append([combined_df['track_id'].iloc[indx], combined_df['artist_names'].iloc[indx], combined_df['track_name'].iloc[indx], np.round(sim_scores[i][1],decimals=3)])
    
    return ranked_tracks