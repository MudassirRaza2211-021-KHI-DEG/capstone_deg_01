# Team name : Data Monks

## Team Members

 
| Name | Rollnumber | Email|
| :------- | :------------: | ----------: |  
|  Muhammad Mudassir Raza |  2211-021-KHI-DEG      |   mohammad.mudassir@xloopdigital.com       |
|  Eraj Khan |  2211-006-KHI-DEG      |   eraj.khan@xloopdigital.com       |
|  Aniqa Masood |  2211-003-KHI-DEG      |   aniqa.masood@xloopdigital.com       |
|  Muhammad Osama |  2211-022-KHI-DEG      |   mohammad.osama@xloopdigital.com      |\
|  Anoosha Malik  |  2211-004-KHI-DEG        |  anoosha.malik@xloopdigital.com |\
|  Syed Saif Ali |  2211-029-KHI-DEG      |   syed.saif@xloopdigital.com       |\
| Shahzaib Khan | 2211-026-KHI-DEG | shahzaib.khan@xloopdigital.com


## Contributions Conventions:
Here we will write conventions for our future use...

High level architecture diagram can be seen [here](https://drive.google.com/file/d/1-ybYa2Y_FydHw2wFDw0f9lePhhrNti4P/view).

About requirements.txt and setup.py:
1) Create `requirements.txt` , create venv, activate it and install requirement.txt in it.
2) Create `setup.py` file , and run pip install . (pip will use setup.py to install your module) , this will 'create Capstone_project_deg_01.egg-info' and 'build' folders.

About Pre-commit
1) To get started with pre-commit we need to install the pre-commit package.
2) The configuration for pre-commit hooks are defined in a .pre-commit-config.yaml file.

Pre-commit is a multi-language package manager for pre-commit hooks. You specify a list of checks (hooks) in a configuration file which will be automatically executed when the git commit command is called. If any of these checks fail, the commit will be aborted allowing you to fix the errors before the code is committed to the repository’s history.
The pre-commit package manages the installation of any required dependencies for your hooks and can even auto-fix any errors (e.g. code formatting) after running the scripts.
