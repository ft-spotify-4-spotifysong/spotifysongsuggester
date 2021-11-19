'''spotify song'''

import pandas as pd
import numpy as np
from flask import Flask, render_template, request
from .suggester import suggester
from .models import DB, Song


def create_app():

    #df = pd.read_csv('songs.csv')  # local flask run
    df = pd.read_csv('spotifysong/songs.csv')  # for Heroku deploy
    songs = df.sort_values(by=['name'])['name'].to_list()
    for s in songs:
        print('------', type(s))
        print(s)
        break

    global suggested_songs
    suggested_songs = []

    APP = Flask(__name__)
    APP.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
    APP.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Give our APP access to our database
    DB.init_app(APP)

    @APP.route("/")
    def root():
        '''query songs'''
        recent_songs_info = []
        recent_songs = Song.query.all()
        recent_songs_info = [
            f'SONG NAME: {s2.name} ------ ALBUM: {s2.album} ------ ARTIST: {s2.artists}' for s2 in recent_songs]
        return render_template('base.html', songs=songs, recent_songs_info=recent_songs_info)

    @APP.route('/suggestsong', methods=['POST'])
    def song():
        # request.values is pulling data from the html
        # use the songname from the URL (route)
        # or grab it from the dropdown menu
        #songn = request.form.get('songname').strip()
        songn = request.form.get('songname')
        suggest_songs_number = request.form.get('suggest_songs_number')
        suggested_songs_info = []
        if songn not in df['name'].to_list():
            return 'Sorry, song is not exist'
        else:
            # require similar songs for input song
            try:
                num = int(suggest_songs_number)
                print(songn, suggest_songs_number)
                response = suggester(songn, df, num)
                if response.empty:
                    return 'Similar songs are not founded'
                else:
                    songs_info = response[['name', 'album', 'artists']]
                    selected_song = songs_info.iloc[0].values
                    selected_song_info = f'SONG NAME: {selected_song[0]} ------ ALBUM: {selected_song[1]} ------ ARTIST: {selected_song[2]}'
                    suggested_songs = songs_info.iloc[1:].values
                    suggested_songs_info = [
                        f'SONG NAME: {suggested_songs[i][0]} ------ ALBUM: {suggested_songs[i][1]} ------ ARTIST: {suggested_songs[i][2]}' for i in range(0, suggested_songs.shape[0])]
                    # refresh database table with suggested songs
                    DB.drop_all()
                    DB.create_all()
                    i = 1
                    for s1 in suggested_songs:
                        print('s1------', s1[0], s1[1], s1[2])
                        db_song = Song(
                            id=i, name=s1[0], album=s1[1], artists=s1[2][1:len(s1[2])-1])
                        DB.session.add(db_song)
                        i += 1
                    DB.session.commit()
            except Exception as e:
                return str(e)
        return render_template('suggested_songs.html',
                               selected_song_info=selected_song_info,
                               suggested_songs_info=suggested_songs_info)

    @APP.route('/reset')
    def reset():
        # remove everything from the database
        DB.drop_all()
        # Creates the database file initially.
        DB.create_all()
        return "reset"

    return APP
