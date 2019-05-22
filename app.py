from flask import Flask, render_template, session, flash, request, abort, redirect, url_for
from scrape_lyrics import scrape, getSong
import spotify_token as st
from datetime import datetime
import time
import os

app = Flask(__name__)
app.secret_key = os.urandom(12)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        username =  request.form['username']
        password = request.form['password']
        data = st.start_session(username, password)
        session['token'] = data[0]
        session['token_exp'] = data[1]
        return redirect(url_for('lyrics'))

    return render_template('login.html')

@app.route('/lyrics')
def lyrics():
    # TODO: Deal with session expiry
    if 'token' not in session: # or session['token_'] < datetime.now():
        # redirects to home so user can log in
        return redirect(url_for('home'))

    song_response = getSong(session['token'])
    return redirect(url_for('search_lyrics'))

    # handle response errors
    if song_response == 204:
        return redirect(url_for('search_lyrics'))

    return render_template('lyrics.html', lyrics=song_response)

@app.route('/search_lyrics', methods=["GET", "POST"])
def search_lyrics():
    if request.method == 'POST':
        song_name =  request.form['song_name']
        song_artist = request.form['song_artist']
        song_response = scrape(song_name, song_artist)
        return render_template('lyrics.html', lyrics=song_response)

    return render_template('search_lyric.html')

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
