# Digital Infrastructure for Research and Extension on Crops and Technology for Agriculture (DIRECT4AG)

This is the service API for the Direct4Ag frontend. 

### Prerequisites
* Python>=3.8
* Make sure [Poetry](https://github.com/python-poetry/poetry) is available in your environment.

### Setup Environment

* Install the dependencies: `poetry install`.
* Create `.env` file in project root (see `.env-example` for the available variables)

Run:
`uvicorn app.main:app --reload`

You should be able to run:
http://localhost:8000/direct4ag for base route that return welcome message
http://localhost:8000/docs for swagger docs

## Docker

### Build docker container

docker build --progress=plain --tag direct4ag/service:latest .

### Run service with docker
See Setup Environment section for populating the direct4ag-env

On Linux, you can run the docker image with the following:

docker run -p 8000:8000 --network host --env-file direct4ag-env direct4ag/service:latest

On Mac and other platforms, use:

docker run -p 8000:8000 --env-file direct4ag-env direct4ag/service:latest

