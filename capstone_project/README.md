# Capstone Project - Room Occupancy Detection

## Overview

This project aims to leverage the power of IoT sensors and machine learning to predict if a room is occupied or not. The system utilizes various IoT sensors, such as temperature sensors, humidity sensors, light sensors, and CO2 sensors, to gather data on various environmental factors in a room.

Your task is to create a pipeline which:
* Collects data from all the sensors
* Transforms & joins sensor data
* Query provided ML model and predicts Occupancy
* Stores result and visualize it

## Rooms

While designing your solution you have access to full apartment equipped in every room with all sensors listed in next section.
Apartment contains rooms with IDs:
* kitchen
* bedroom
* living_room
* bathroom

## Sensors

This section contains description about various sensors used in this project.

### SmartThermo

SmartThermo is an IoT temperature sensor that collects temperature data every minute and records it in degrees Fahrenheit. The sensor utilizes advanced temperature sensing technology to ensure high precision and accuracy. The collected data is then securely saved to an S3 bucket, allowing for easy access and analysis. With SmartThermo, users can monitor temperature changes in real-time and make data-driven decisions to optimize their environment.

SmartThermo sensor saves the temperature data in a structured format, as a CSV file.
Each data point recorded by the sensor includes the following information:

* Temperature: The measured temperature in degrees Fahrenheit
* Timestamp: The date and time that the temperature measurement was taken
* Room ID: An identifier for the room where the temperature measurement was taken.

Data is stored in desired S3 bucket in path: `s3://BUCKET/smart_thermo/2022-01-10T10:31:00.csv`

For example data might be organized like these:
```csv
temperature,timestamp,room_id
72.5,2022-10-01T09:30:00,kitchen
```


### MoistureMate

MoistureMate is an advanced humidity sensor that delivers real-time data on the moisture levels in your environment. With its cutting-edge sensing technology and intuitive design, MoistureMate is the ultimate tool for monitoring and maintaining optimal humidity levels in any setting. Whether you're monitoring a grow room, ensuring proper humidity in a museum, or simply keeping your home comfortable, MoistureMate has got you covered.

The sensor is also designed to send the data via an HTTP POST request in JSON format to a configurable endpoint. The JSON payload includes the following information:

* Humidity: The measured humidity in percent (e.g. 30.5)
* Humidity Ratio: The ratio of water vapor to dry air (e.g. 0.01)
* Timestamp: The date and time that the humidity measurement was taken
* Room ID: An identifier for the room where the humidity measurement was taken.

For example, the data might be organized like this in JSON format:
```json
{
  "humidity": 30.5,
  "humidity_ratio": 0.01,
  "timestamp": "2022-10-01T09:30:00",
  "room_id": "bedroom"
}
```

### LuxMeter

LuxMeter is a next-generation light sensor that provides unparalleled precision and accuracy in measuring light levels. This device equipped with advanced photodiodes and filtering technology, providing a full spectral response and making it suitable for any lighting conditions. With LuxMeter you can track the light intensity and compare it to the recommended levels, getting insights on energy consumption and well-being of your environment.

You can access the data using a simple RESTful API, simply by making a GET request to the endpoint `/api/luxmeter/<room_id>` which returns last 15 measurements containing light level and timestamp in JSON format.

For example calling endpoint `/api/luxmeter/living_room` may return:

```json
{
  "room_id": "living_room",
  "measurements": [
    {
      "timestamp": "2022-10-01T09:15:00",
      "light_level": 310
    },
    //... other measurements
    {
      "timestamp": "2022-10-01T09:30:00",
      "light_level": 350
    }
  ]
}



```

### CarbonSense

CarbonSense is a top-of-the-line carbon dioxide sensor designed to give you the most accurate and real-time data on CO2 levels in your environment. Whether you're monitoring air quality in a commercial greenhouse, a classroom or an office building, CarbonSense has got you covered. The sensor is equipped with advanced non-dispersive infrared (NDIR) technology to measure CO2 levels, and able to send data to a configurable endpoint via HTTP POST request in JSON format.

Sample payload may look like that:
```json
{
  "co2": 400,
  "timestamp": "2022-10-01T09:30:00",
  "room_id": "bedroom"
}
```

## Model

Code for ML Model used in this project is provided in `./model` directory.
Model can be trained using publicly available [dataset](https://www.kaggle.com/datasets/kukuroo3/room-occupancy-detection-data-iot-sensor).

You can run the training using run_train.py


- `data_path` is the path to the .csv dataset file.
- `save_model` boolean argument determining whether to save the model as a pickle file.
- `model_dir` is the dir in which the model will be saved.

## Running Sensors

Run docker-compose project located inside `./sensors` directory.

You should configure these variables located inside `./sensors/docker-compose.yml`:
* SMART_THERMO_BUCKET - name of the bucket that will be populated by SmartThermo
* MOISTURE_MATE_URL - endpoint url for collecting MoistureMate data
* CARBON_SENSE_URL - endpoint url for collecting CarbonSense data
* AWS_ACCESS_KEY_ID - your AWS access key (used to access S3 bucket)
* AWS_SECRET_ACCESS_KEY - your AWS secret key (uset to access S3 bucket)


## Tips

* Note that model training data uses temperature in Celsius degrees
* Deploying sensor to your project infrastructure may be a good idea
