# Medical-Rec

## Description

Medical-Rec is a RESTful service that allows doctors and medical professionals to access and update a patient's medical history. The service allows for basic CRUD operations, including creating new patient records, retrieving existing patient records, updating existing patient records, and deleting patient records.

---
## Installation

> To install the Medical-Rec service, you will need Python 3.10.11 and Postgresql 14 version.

There are two installation methods available:
- [Installing with docker compose](#docker-installation)
- [Installing on the host machine](#local-installation)

Before installation, create a .env file from the provided env-example file. In the .env file, provide values for the following environment variables:

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
1. For Docker installation, make sure that you have Docker Compose pre-installed on your machine. Configure desired environment variables in the [docker-compose file](https://github.com/RDonii/medical-rec/blob/0078bb2decdfb50f01d8a19229228cbefb92edef/docker-compose.yml#L6) for the database service. They must be the exact same as in the .env file. Run the following command to start the service:

2. Run following command:
    ```
        docker compose up
    ```
The service will run on port 80 of your machine.

### Local installation

For local installation, it is suggested to activate a virtual Python environment such as pipenv, virtualenv, or conda.
1. Set DEBUG=True to serve static and media files on the development server.

2. Create a database.

3. Install dependencies

    ```
        pip install -r requirements.txt
    ```

4. Migrate tables and run the development server with the following commands:

    ```
        python manage.py migrate
        python manage.py runserver
    ```
---
## Usage

API documentation URLs:
- Swagger: /doc/swagger-ui
- ReDoc: /doc/redoc

---
## Testing

> Note: If you used the Docker Compose installation method, the test service runs all tests before running the web service.

For testing, use the [PyTest](https://docs.pytest.org/en/7.3.x/) framework.
Run all tests with the following command:


        pytest
        

Alternatively, use the preconfigured testing tab of VSCode.
