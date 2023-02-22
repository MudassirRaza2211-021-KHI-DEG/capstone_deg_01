import json
import logging
import os
import pickle

import pandas as pd
import psycopg2
import requests
from flask import Flask, json, jsonify, render_template, request

app = Flask(__name__)

logger = logging.getLogger()

with open('capstone_deg_01/model/trained_model/model.pkl', 'rb') as file:
    model = pickle.load(file)

postgres_user = os.environ.get("POSTGRES_USER")
postgres_password = os.environ.get("POSTGRES_PASSWORD")
postgres_db = os.environ.get("POSTGRES_DB")
postgres_ip = os.environ.get("POSTGRES_IP")


def connect():
    conn = psycopg2.connect(database=postgres_db, user=postgres_user,
                            password=postgres_password, host=postgres_ip, port="5432")

    cur = conn.cursor()
    cur.execute(
        "SELECT DISTINCT ON (room_id) * FROM mytable ORDER BY room_id, timestamp DESC")
    results = cur.fetchall()
    return results


def get_predictions():

    df = connect()
    df = pd.DataFrame(df, columns=[
                      'timestamp', 'room_id', 'humidity', 'humidity_ratio', 'co2', 'light_level', 'temperature'])

    d = df[["temperature", "humidity", "light_level", "co2", "humidity_ratio"]]
    predictions = model.predict(d)
    df_predic = pd.DataFrame(predictions, columns=['predictions'])
    result = pd.merge(df_predic, df, left_index=True, right_index=True)

    return result


def prediction_name_and_temperature_conversion():

    result_df = predictions()
    result_df['room_id'] = result_df['room_id'].replace(
        {'living_room': 'Cardiology', 'kitchen': 'Pediatrics', 'bathroom': 'Private Ward', 'bedroom': 'CCU'})
    result_df['predictions'] = result_df['predictions'].replace(
        {0: 'Not Occupied', 1: 'Occupied'})
    result_df['temperature'] = (result_df['temperature'] - 32) * 5/9

    json_data = result_df.to_json(date_format='iso', orient='records')
    logger.info(f"json_data {json_data}")
    return json_data


@app.route('/data/api/endpoint', methods=['GET', 'POST'])
def send_data():
    data = json.loads(prediction_name_and_temperature_conversion())
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
    app.run(debug=True, port=8000, host="0.0.0.0")
    logging.basicConfig(level=logging.INFO)
    prediction_name_and_temperature_conversion()