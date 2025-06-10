from flask import Flask, render_template
from dotenv import load_dotenv
import os

app = Flask(__name__)

load_dotenv('key.env')

@app.route('/')
def home():
    API_KEY = os.getenv("API_KEY") 
    return render_template('Gen_flashcards_v2.html', api_key=API_KEY)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
