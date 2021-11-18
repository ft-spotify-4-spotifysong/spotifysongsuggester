'''spotify song'''

import pandas as pd
from flask import Flask, render_template, request
from .suggester import suggester


def create_app():

    # original_df = pd.read_csv('original.csv')  # local flask run
    # df = pd.read_csv('spotify.csv')  # local flask run
    original_df = pd.read_csv('spotifysong/original.csv')  # for Heroku deploy
    df = pd.read_csv('spotifysong/spotify.csv')  # for Heroku deploy
    songs = df['name'].to_list()
    for s in songs:
        print('------', type(s))
        print(s)
        break

    APP = Flask(__name__)
    APP.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
    APP.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    @APP.route("/")
    def root():
        '''query songs'''
        return render_template('base.html', songs=songs)

    @APP.route('/suggestsong', methods=['POST'])
    def song():
        # request.values is pulling data from the html
        # use the songname from the URL (route)
        # or grab it from the dropdown menu
        #songn = request.form.get('songname').strip()
        songn = request.form.get('songname')
        suggest_songs_number = request.form.get('suggest_songs_number')
        suggest_songs = []
        suggested_songs_info = []
        if songn not in df['name'].to_list():
            suggested_songs_info = ['Sorry, song is not exist']
        else:
            # require similar songs for input song
            try:
                num = int(suggest_songs_number)
                print(songn, suggest_songs_number)
                response = suggester(songn, df, num)
                if response.empty:
                    suggested_songs_info = ['there is no suggest songs']
                else:
                    suggest_songs = response['songname'].to_list()
                    indexes = response['neighbors'].to_list()
                    suggest_songs_albums = [
                        original_df.iloc[int(i)]['album'] for i in indexes]
                    suggest_songs_artists = [
                        original_df.iloc[int(i)]['artists'] for i in indexes]
                    suggested_songs_info = [
                        f'SONG NAME: {suggest_songs[i]} ------ ALBUM: {suggest_songs_albums[i]} ------ ARTIST: {suggest_songs_artists[i][1:len(suggest_songs_artists[i])-1]}' for i in range(0, len(suggest_songs))]
                    print('suggest_songs_info: ', suggested_songs_info)
            except Exception as e:
                return str(e)
        return render_template('suggested_songs.html', songname=songn, suggested_songs_info=suggested_songs_info)

    return APP
