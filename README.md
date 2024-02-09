# Digital Infrastructure for Research and Extension on Crops and Technology for Agriculture (DIRECT4AG)

This is the service API for the Direct4Ag frontend. 

## Set up

### Prerequisites `Python>=3.10`

* Make sure [Poetry](https://github.com/python-poetry/poetry) is available in your environment.
* Install the dependencies:
  * `poetry install`.
* Create a PostgreSQL (>= v13) database with the following extensions:
  * PostGIS (>= v3.1): `CREATE EXTENSION postgis`
* Create `.env` file in project root (see `.env-example` for the available variables).
* Create tables replace `<message>` with your message:
  * `poetry run ./scripts/migrations_create.sh <message>`
* Now apply the migrations:
  * `poetry run ./scripts/migrations_forward.sh`.
* Run the dev server:
  * `poetry run ./scripts/run_dev_server.sh`.

You should be able to run:
http://localhost:8000/api/docs for swagger docs

### Database migrations

Migrations are managed by `alembic`. All revisions are in `alembic/versions`.

After adding new models or updating the existing ones, you need to create new migrations by running `poetry run ./scripts/migrations_create.sh "<Migration Message>"`.

To apply the new changes to an existing database, run `poetry run ./scripts/migrations_forward.sh`.

You can revert to a specific migration by running `poetry run ./scripts/migrations_reverse.sh <migration-id>`.
You can find the ID for each migration in its file in `alembic/versions`.

## Docker

### Build docker container

docker build --progress=plain --tag direct4ag/service:latest .

### Run service with docker

See Setup Environment section for populating the direct4ag-env

On Linux, you can run the docker image with the following:

docker run -p 8000:8000 --network host --env-file direct4ag-env direct4ag/service:latest

On Mac and other platforms, use:

docker run -p 8000:8000 --env-file direct4ag-env direct4ag/service:latest

