'''suggest songs according to user's input song'''
import pandas as pd
import numpy as np
#from sklearn import preprocessing
from sklearn import neighbors


def suggester(song_name, songs_df, neighbors_number):
    '''get similar songs'''

    if song_name not in songs_df['name'].to_list():
        return None

    # buile model
    X = songs_df.drop(columns=['name', 'album', 'artists']).values
    model = neighbors.NearestNeighbors(n_neighbors=min(
        neighbors_number+1, X.shape[0]))
    model.fit(X)

    # get suggest songs
    print(song_name, songs_df[songs_df['name'] == song_name])
    select_song_index = songs_df[songs_df['name'] == song_name].index[0]
    select_song_array = np.array(
        songs_df.drop(columns=['name', 'album', 'artists']).iloc[select_song_index]).reshape(1, -1)

    distance, neighbors_indexes = model.kneighbors(select_song_array)

    if distance == []:
        return []

    # prepare output file for suggested songs
    suggest_songs,  suggest_songs_album, suggest_songs_artists = [], [], []
    for index_i in neighbors_indexes[0]:
        suggest_songs.append(songs_df['name'].iloc[index_i])
        suggest_songs_album.append(songs_df['album'].iloc[index_i])
        suggest_songs_artists.append(songs_df['artists'].iloc[index_i])

    output = pd.DataFrame(
        {'name': suggest_songs, 'album': suggest_songs_album,
            'artists': suggest_songs_artists,
         'distance': list(distance[0]),
         'neighbors': list(neighbors_indexes[0])})
    output.to_csv('output.csv')
    #print('suggest songs: ', output)

    # prepare correlation graph array for suggested songs
    check_arrays = X[neighbors_indexes[0], :]
    graph_array = neighbors.kneighbors_graph(check_arrays, 10, mode='connectivity',
                                             include_self=True).toarray()
    print('------graph array:', graph_array)
    pd.DataFrame(graph_array, columns=suggest_songs).to_csv('correlation.csv')

    return output
