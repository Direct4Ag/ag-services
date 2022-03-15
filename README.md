# Digital Infrastructure for Research and Extension on Crops and Technology for Agriculture (DIRECT4AG)

This is the service API for the frontend. 

# README UNDER CONSTRUCTION
### Prerequisites
* Python>=3.8
* PyTorch>=1.7 (if you want to run the object classification models)

A very simple object detection and classification service using FastAPI

To run, install dependencies using poetry ```poetry install``` or follow the manual installation instructions at 
the end of the file.

Once you are done installing the dependencies, add your database variables (you can find them in `core/config.py`) to your local env variables.

For more info about connection strings click [here](https://stackoverflow.com/a/20722229).

I recommend using PyCharm to run the service. Once you installed the dependencies, add the env created above to the
project's interpreter and run main.py. If not, navigate to the parent directory of main.py and run 
`uvicorn app.main:app --reload`

Once it's running, navigate to `http://0.0.0.0:8000/docs` to run examples.

To manually install the dependencies: 
or:
1. Start from a Python>=3.8 environment with PyTorch>=1.7 installed.
To install PyTorch see https://pytorch.org/get-started/locally/. 
2. Install fastpi: ```pip install fastapi```
3. Install ASGI Server: ```pip install "uvicorn[standard]"```
4. Install YOLOv5 dependencies:
```pip install -qr https://raw.githubusercontent.com/ultralytics/yolov5/master/requirements.txt``` 
5. Install psycopg2:```pip install psycopg2```
6. Install databases: ```pip install databases```


Resources: 
* https://pytorch.org/hub/ultralytics_yolov5/
* https://learnopencv.com/

# Docker

## Build docker container

docker build --progress=plain --tag direct4ag/service:latest .

## Setup Environment

Look at env-example for an example environment file and update parameters with your settings

## Run service with docker

On Linux, you can run the docker image with the following:

docker run -p 8000:8000 --network host --env-file direct4ag-env direct4ag/service:latest

On Mac and other platforms, use:

docker run -p 8000:8000 --env-file direct4ag-env direct4ag/service:latest

