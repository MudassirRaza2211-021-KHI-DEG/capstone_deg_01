# Team name : Data Monks
![Teams-Logo](team-non-technical-files/logo.png)

## Team Members

| Name | Rollnumber | Email|
| :------- | :------------: | ----------: |  
|  Muhammad Mudassir Raza |  2211-021-KHI-DEG |   mohammad.mudassir@xloopdigital.com |
|  Eraj Khan              |  2211-006-KHI-DEG |   eraj.khan@xloopdigital.com         |
|  Aniqa Masood           |  2211-003-KHI-DEG |   aniqa.masood@xloopdigital.com      |
|  Muhammad Osama         |  2211-022-KHI-DEG |   mohammad.osama@xloopdigital.com    |
|  Syed Saif Ali          |  2211-029-KHI-DEG |   syed.saif@xloopdigital.com         |
| Shahzaib Khan           | 2211-026-KHI-DEG  | shahzaib.khan@xloopdigital.com       |

## Project Vision

To automate the hospital rooms by getting predicting the data of occupation by IOT sensors and controlling the appliances of room automatically. 

A high level diagram from end-user perspective can be seen here.

![Business-component-diagram](team-non-technical-files/business-objective.jpg)

## Contributions Conventions:
Here we will write conventions for our future use...

About requirements.txt and setup.py:
1) Create `requirements.txt` , create venv, activate it and install requirement.txt in it.
2) Create `setup.py` file , and run pip install . (pip will use setup.py to install your module) , this will 'create Capstone_project_deg_01.egg-info' and 'build' folders.

## How to Run:
1) Create a volume for MinIO: `docker volume create minio-data`
2) Execute the start_app.sh to run our whole app using `./start_app.sh`