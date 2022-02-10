A very simple object detection and classification service using FastAPI

To run, install dependencies using poetry ```poetry install``` or follow the manual installation instructions at 
the end of the file.

Once you are done installing the dependencies, to setup the database connection, add the db url in config.py. 

For example, 
`postgres_db_url: str = "postgresql://user:pass@localhost:5432/dbname"`

For more info about connection strings click [here](https://stackoverflow.com/a/20722229).

I recommend using PyCharm to run the service. Once you installed the dependencies, add the env created above to the
project's interpreter and run main.py. If not, navigate to the parent directory of main.py and run 
`uvicorn ag-services.main:app --reload`

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