from flask import Flask, request, jsonify, json, render_template, url_for
import requests
import pickle
import pandas as pd
from time import sleep
import psycopg2
import logging
import json
import pandas as pd
import os

app = Flask(__name__)

with open('capstone_deg_01/model/trained_model/model.pkl', 'rb') as file:
    model = pickle.load(file)

postgres_user = os.environ.get("POSTGRES_USER")
postgres_password = os.environ.get("POSTGRES_PASSWORD")
postgres_db = os.environ.get("POSTGRES_DB")
postgres_ip = os.environ.get("POSTGRES_IP")

def connect():
    conn = psycopg2.connect(database=postgres_db, user=postgres_user, password=postgres_password, host=postgres_ip, port="5432")

    cur = conn.cursor()
    cur.execute("SELECT DISTINCT ON (room_id) * FROM mytable ORDER BY room_id, timestamp DESC")
    results = cur.fetchall()
    df = pd.DataFrame(results, columns=['timestamp', 'room_id', 'humidity', 'humidity_ratio', 'co2', 'light_level', 'temperature'])

    df['temperature'] = (df['temperature'] - 32) * 5/9
    d = df[["temperature", "humidity", "light_level", "co2", "humidity_ratio"]]

    predictions = model.predict(d)
    df_predic = pd.DataFrame(predictions, columns=['predictions'])
    result = pd.merge(df_predic, df, left_index=True, right_index=True)
    result['room_id'] = result['room_id'].replace({'living_room': 'Cardiology', 'kitchen': 'Pediatrics', 'bathroom': 'Private Ward', 'bedroom': 'CCU'})
    result['predictions'] = result['predictions'].replace({0: 'Not Occupied', 1: 'Occupied'})

    json_data = result.to_json(date_format='iso', orient='records')
    logger.info(f"json_data {json_data}")
    return json_data

@app.route('/data/api/endpoint', methods=['GET','POST'])
def send_data():
    data = json.loads(connect())
    room_ids = list(set([item['room_id'] for item in data]))
    selected_room = request.form.get('room_id') or room_ids[0]
    room_data = [item for item in data if item['room_id'] == selected_room]

    return render_template('index.html', room_data=room_data, room_ids=room_ids, selected_room=selected_room)

@app.route('/lottie-animation-1')
def lottie_animation_1():
    url = 'https://assets9.lottiefiles.com/packages/lf20_olluraqu.json'
    animation_data = requests.get(url).json()
    return jsonify(animation_data)

@app.route('/lottie-animation-2')
def lottie_animation_2():
    url = 'https://assets8.lottiefiles.com/packages/lf20_GGbnvx.json'
    animation_data = requests.get(url).json()
    return jsonify(animation_data)

@app.route('/lottie-animation-3')
def lottie_animation_3():
    url = 'https://assets3.lottiefiles.com/packages/lf20_9Rpr7C.json'
    animation_data = requests.get(url).json()
    return jsonify(animation_data)

@app.route('/lottie-animation-4')
def lottie_animation_4():
    url = 'https://assets5.lottiefiles.com/packages/lf20_vwoauv0p.json'
    animation_data = requests.get(url).json()
    return jsonify(animation_data)

@app.route('/lottie-animation-5')
def lottie_animation_5():
    url = 'https://assets10.lottiefiles.com/packages/lf20_nfxa6agk.json'
    animation_data = requests.get(url).json()
    return jsonify(animation_data)

if __name__ == '__main__':
    logger = logging.getLogger()
    logging.basicConfig(level=logging.INFO)
    app.run(debug=True, port=8000, host="0.0.0.0")
