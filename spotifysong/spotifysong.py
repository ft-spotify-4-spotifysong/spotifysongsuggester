'''spotify song'''

import pandas as pd
from flask import Flask, render_template, request
from .suggester import suggester


def create_app():

    df = pd.read_csv('spotify/spotify.csv')
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
        return render_template('base.html', title="home",
                               songs=songs)

    @APP.route('/suggestsong', methods=['POST'])
    def song():
        # request.values is pulling data from the html
        # use the songname from the URL (route)
        # or grab it from the dropdown menu
        songn = request.form.get('songname').strip()
        suggest_songs_number = request.form.get('suggest_songs_number')
        suggest_songs = []
        if songn not in df['name'].to_list():
            message = message = 'Sorry, song is not exist'
        else:
            # require similar songs for input song
            try:
                num = int(suggest_songs_number)
                print(songn, suggest_songs_number)
                response = suggester(songn, df, num)
                print('response-------', response, type(response))
                if response.empty:
                    message = 'there is no suggest songs'
                else:
                    suggest_songs = response['name'].to_list()
                    print('suggest songs------', suggest_songs)
                    message = 'suggested songs:'
            except Exception as e:
                return str(e)
        return render_template('suggested_songs.html', title='suggest songs', suggest_songs=suggest_songs, message=message)

    return APP
