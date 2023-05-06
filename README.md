# Medical-Rec

## Description

RESTful service that allows doctors and medical professionals to access and update a patient's medical history. The service allows for basic CRUD operations, including creating new patient records, retrieving existing patient records, updating existing patient records, and deleting patient records.

---
## Installation

> Project built and tested with python 3.10.11 and Postgresql 14 version

There are two way of installations provided.
- [installing with docker compose](#docker-installation)
- [installing on host machine](#local-installation)

On both ways, the first step is creating .env file from env-example file. Here is some explenations for the environment variables:

|variable name|reuqired|description|
|---|---|---|
|SECRET_KEY|✅|secret key for the Django application|
|HOSTS|✅ (at least one)|hosts to serve api|
|CORS_ALLOWED_ORIGINS|✅ (at least one)|allowed cross origins for resourse sharing|
|JWT_ACCESS_TOKEN_LIFETIME|❌(default=0.5)|life time of access json web token in hours|
|JWT_REFRESH_TOKEN_LIFETIME|❌(default=24)|life time of access json web token in hours|
|DEBUG|❌(default=false)|debugging mode|
|FRONTEND_PASSWORD_RESET_CONFIRM_URL|❌|password reset confirmation url of frontend to send on email|
|FRONTEND_USERNAME_RESET_CONFIRM_URL|❌|username reset confirmation url of frontend to send on email|
|DB_NAME|✅|database name|
|DB_USER|✅|database user|
|DB_PASSWORD|✅|password of database user|
|DB_PORT|✅|database port|
|DB_HOST|✅|database host (do not change if you are using docker installation method)|


### Docker installation

You must have docker compose preinstalled on your machine.
1. Configure desired environment variables in [docker-compose file](https://github.com/RDonii/medical-rec/blob/0078bb2decdfb50f01d8a19229228cbefb92edef/docker-compose.yml#L6) for db service. They must be exact same as in .env file.
2. Run following command:
    ```
        docker compose up
    ```
Project will run on 80 port of your machine.

### Local installation

1. Suggested firstly activate virtual python environment, such as pipenv, virtualenv or conda.
2. Set DEBUG=True in order to serve static and media files on development server
3. Create Database
4. Install dependencies. 
    ```
        pip install -r requirements.txt
    ```
5. Run development server
    ```
        python manage.py runserver
    ```
---
## Usage

API documentation urls:
- Swagger: /doc/swagger-ui
- ReDoc: /doc/redoc

---
### Testing

For the testing [PyTest](https://docs.pytest.org/en/7.3.x/) framework user.
To run all tests, run following command:
    ```
        pytest
    ```
or use prevonfigured testing tab of Viescode.
