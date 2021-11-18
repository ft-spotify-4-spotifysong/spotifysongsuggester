'''suggest songs according to user's input song'''
import pandas as pd
import numpy as np
from sklearn import preprocessing
from sklearn import neighbors
#from sklearn.neighbors import NearestNeighbors
#import joblib

example_song = 'Sleep Now In the Fire'


def suggester(song_name, songs_df, neighbors_number):
    '''get similar songs'''

    if song_name not in songs_df['name'].to_list():
        return None

    # buile model
    X = songs_df.drop(columns=['name']).values
    model = neighbors.NearestNeighbors(n_neighbors=min(
        neighbors_number+1, X.shape[0]))
    model.fit(X)

    # get suggest songs
    print(song_name, songs_df[songs_df['name'] == song_name])
    select_song_index = songs_df[songs_df['name'] == song_name].index[0]
    print(select_song_index)
    select_song_array = np.array(
        songs_df.drop(columns=['name']).iloc[select_song_index]).reshape(1, -1)
    print('-------', select_song_array)

    suggest_songs = []
    distance, neighbors_indexes = model.kneighbors(select_song_array)

    if distance == []:
        return []

    for index_i in neighbors_indexes[0][1:]:
        suggest_songs.append(
            songs_df['name'].iloc[index_i])

    suggest_songs_df = pd.DataFrame(
        data=suggest_songs, columns=['name'])

    output = pd.DataFrame(
        {'songname': suggest_songs, 'distance': list(distance[0][1:]), 'neighbors': list(neighbors_indexes[0][1:])})
    output.to_csv('output.csv')

    print('suggest songs: ', output)
    return output
