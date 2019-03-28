from flask import Flask, jsonify
from scrape_lyrics import scrape

app = Flask(__name__)

@app.route('/')
def index():
    return scrape()

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
