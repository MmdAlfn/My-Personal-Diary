import os
from os.path import join, dirname
from dotenv import load_dotenv
from flask import Flask, render_template, jsonify, request
from pymongo import MongoClient
from datetime import datetime

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

MONGODB_URI = os.environ.get("MONGODB_URI")
DB_NAME =  os.environ.get("DB_NAME")

client = MongoClient(MONGODB_URI)
db = client[DB_NAME]

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/diary', methods=['GET'])
def show_diary():
    articles = list(db.diary.find({}, {'_id':False}))
    return jsonify({'articles': articles})

@app.route('/diary', methods=['POST'])
def post_diary():
    title_receive = request.form.get('title_give')
    content_receive = request.form.get('content_give')
    
    today = datetime.now()
    mytime = today.strftime('%Y-%m-%d_%H-%M-%S')
    post_time = today.strftime('%Y-%m-%d_%H.%M')
    
    file = request.files['file_give']
    extension = file.filename.split('.')[-1]
    filename = f'static/post-{mytime}.{extension}'
    file.save(filename)
    
    profile = request.files['profile_give']
    extension_profile = profile.filename.split('.')[-1]
    profilename = f'static/profile-{mytime}.{extension_profile}'
    profile.save(profilename)
    
    doc = {
        'File': filename,
        'Profile': profilename,
        'Judul': title_receive,
        'Komentar': content_receive,
        'Waktu Post': post_time
    }
    
    db.diary.insert_one(doc)
    
    return jsonify({'msg': 'Data saved'})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)