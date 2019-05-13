from flask import Flask, render_template, session, flash, request, abort, redirect, url_for
from scrape_lyrics import scrape, getSong
import spotify_token as st
from datetime import datetime
import time
import os

app = Flask(__name__)
app.secret_key = os.urandom(12)

@app.route('/', methods=["GET", "POST"])
def home():
    if request.method == 'POST':
        username =  request.form['username']
        password = request.form['password']
        data = st.start_session(username, password)
        session['token'] = data[0]
        session['token_exp'] = data[1]
        return redirect(url_for('lyrics'))

    return render_template('index.html')

@app.route('/lyrics')
def lyrics():
    # TODO: Deal with session expiry
    if 'token' not in session: # or session['token_'] < datetime.now():
        # redirects to home so user can log in
        return redirect(url_for('home'))

    return render_template('lyrics.html', lyrics=getSong(session['token']))

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
