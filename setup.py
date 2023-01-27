from setuptools import find_packages, setup

setup(
    name='Capstone_project_deg_01',
    version='1.0',
    author='SSAAEMO',
    description='Capstone_project_deg_01',
    long_description='This project aims to leverage the power of IoT sensors and machine learning to predict if a room is occupied or not. The system utilizes various IoT sensors, such as temperature sensors, humidity sensors, light sensors, and CO2 sensors, to gather data on various environmental factors in a room.',
    url='https://github.com/MudassirRaza2211-021-KHI-DEG/capstone_deg_01',
    python_requires='>=3.7, <4',
    packages=find_packages(),
    install_requires=[
        'numpy>=1.14.5'
    ],

)
