# django-recruitment-ffg
Django/DRF REST API for uploading and serving images

[![Pytest](https://github.com/hector97i/django-recruitment-ffg/actions/workflows/pytest.yml/badge.svg)](https://github.com/hector97i/django-recruitment-ffg/actions/workflows/pytest.yml)

## Installation

This project uses `poetry` to manage dependencies and other project functionalities.

1. Install poetry (Linux, MacOS, WSL)
    ```shell
    curl -sSL https://install.python-poetry.org | python3 -
    ```

1. Install project, if there is no venv activated, poetry will create a new venv for it [info here](https://python-poetry.org/docs/managing-environments/).
    ```bash
    poetry config --local virtualenvs.in-project true
    poetry install
    ```

1. Activate .venv
    ```bash
    source .venv/bin/activate
    ```

3. Configure project by creating a `config.json` file in the root of the project using this structure:
    ```json
    {
        "ENVIRONMENT": "DEVELOPMENT", // environment to run in
        "SECRET_KEY": "xxxxxx", // django secret key
        "DEBUG": true,
        "BASE_URL": "http://localhost:8000",
        "DB": { // db config
            "ENVIRONMENT": "DEVELOPMENT",
            "RDBMS": "sqlite3", // one of sqlite3 or postgresql
            "NAME": "",
            "USER": "",
            "PASSWORD": "",
            "HOST": "", // if running in docker-compose, use "postgres" (name of the service)
            "PORT": "5432"
        },
        "ALLOWED_HOSTS": [ // security, whitelist and cors config
            "*"
        ],
        "CORS": {
            "ALLOWED_ALL": true,
            "ALLOWED_ORIGINS": [],
            "COOKIE_SECURE": false
        },
        "AWS": { // aws credentials and bucket name
            "ACCESS_KEY_ID": "AKIAQS7OEXBKBMRK7KJN",
            "SECRET_ACCESS_KEY": "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",
            "STORAGE_BUCKET_NAME": "image-app-finmancorp",
            "REGION_NAME": "us-east-2",
            "USE_S3": false // if true, host staticfiles in s3
        },
        // in case you dont' want your static files hosted on s3
        "STATIC_ROOT_PATH": "/var/www/html/static",
        "MEDIA_ROOT_PATH": "/var/www/html/media"
    }
    ```
4. Run with `python manage.py runserver` for local development or run in docker using `docker-compose up --build -d`
