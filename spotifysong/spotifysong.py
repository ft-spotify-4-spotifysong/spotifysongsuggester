'''spotify song'''

import pandas as pd
import numpy as np
from flask import Flask, render_template, request
from .suggester import suggester
from .models import DB, Song
import os
from .plot import plot_correlation, plot_distance


def create_app():

    #df = pd.read_csv('songs.csv')  # local flask run
    df = pd.read_csv('spofitysong/songs.csv')  # for Heroku deploy
    songs = df.sort_values(by=['name'])['name'].to_list()
    for s in songs:
        print('------', type(s))
        print(s)
        break

    #APP = Flask(__name__, static_url_path='', static_folder='/static')
    APP = Flask(__name__)
    APP.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
    APP.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Give our APP access to our database
    DB.init_app(APP)

    def return_image_stream(image_path):
        import base64
        image_stream = ''
        with open(image_path, 'rb') as img_f:
            img_stream = img_f.read()
            img_stream = base64.b64encode(img_stream).decode()
        return img_stream

    @APP.route("/")
    def root():
        '''query songs'''
        recent_songs_info = []
        recent_songs = Song.query.all()
        recent_songs_info = [
            f'SONG NAME: {s2.name}-------ALBUM: {s2.album}-------ARTIST: {s2.artists}' for s2 in recent_songs]
        return render_template('base.html', songs=songs, recent_songs_info=recent_songs_info)

    @APP.route('/suggestsong', methods=['POST'])
    def song():
        # request.values is pulling data from the html
        # use the songname from the URL (route)
        # or grab it from the dropdown menu
        # songn = request.form.get('songname').strip()
        songn = request.form.get('songname')
        suggest_songs_number = request.form.get('suggest_songs_number')
        if songn not in df['name'].to_list():
            return 'Sorry, song is not exist'
        else:
            # require similar songs for input song
            try:
                if suggest_songs_number == '':
                    num = 20
                else:
                    num = int(suggest_songs_number)
                response = suggester(songn, df, num)
                if response.empty:
                    return 'Similar songs are not founded'
                else:
                    songs_info = response[['name', 'album', 'artists']]
                    selected_song = songs_info.iloc[0].values
                    selected_song_info = f'SONG NAME: {selected_song[0]}-------ALBUM: {selected_song[1]}-------ARTIST: {selected_song[2][1:len(selected_song[2])-1]}'
                    suggested_songs = songs_info.iloc[1:].values
                    suggested_songs_names = songs_info['name'].to_list()[1:]
                    # refresh database table with suggested songs
                    DB.drop_all()
                    DB.create_all()
                    i = 1
                    for s1 in suggested_songs:
                        db_song = Song(
                            id=i, name=s1[0], album=s1[1], artists=s1[2][1:len(s1[2])-1])
                        DB.session.add(db_song)
                        i += 1
                    DB.session.commit()
                    plot_correlation()
                    #plot_distance()
            except Exception as e:
                return str(e)
        return render_template('suggested_songs.html',
                               selected_song_info=selected_song_info,
                               suggested_songs_names=suggested_songs_names, num=len(suggested_songs_names))

    @APP.route('/suggestsongsinfo')
    def suggestsongsinfo():
        '''show all songs information'''
        suggested_songs = Song.query.all()
        print('suggestedsongsinfo -------', suggested_songs)
        suggested_songs_info = [
            f'SONG NAME: {s2.name}-------ALBUM: {s2.album}-------ARTIST: {s2.artists}' for s2 in suggested_songs]
        num = len(suggested_songs_info)
        return render_template('suggested_songs_info.html', suggested_songs_info=suggested_songs_info, num=num)

    @APP.route('/reset')
    def reset():
        # remove everything from the database
        DB.drop_all()
        # Creates the database file initially.
        DB.create_all()
        return "reset"

    return APP
