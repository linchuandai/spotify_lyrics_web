from flask import Flask, render_template, session, flash, request, abort, redirect
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

@app.route('/lyrics')
def lyrics():
    token = None
    # need to retrieve login information from login
    username = ''
    password = ''
    if token is None: #or token_exp < datetime.now():
        data = st.start_session(username, password)
        token = data[0]
        token_exp = data[1]

    return render_template('lyrics.html', lyrics=getSong(token))
    # return render_template('lyrics.html', lyrics=scrape('', ''))

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
