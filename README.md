# Geo Notes

Geo Notes is a web application that allows users to create, view, update, and delete points of interest on a map. Users can register and login to manage their personal points of interest. The application uses Django for the backend and React for the frontend. The project is containerized using Docker. The focus of this application is primarily on the backend side of the application.

## Table of Contents

- [Geo Notes](#geo-notes)
  - [Table of Contents](#table-of-contents)
  - [Scope](#scope)
  - [Project Structure](#project-structure)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Running the Application](#running-the-application)
  - [Environment Variables](#environment-variables)
  - [Usage](#usage)
  - [API Endpoints](#api-endpoints)
  - [Test](#test)

## Scope
1. This repository focuses on the Django backend more than the React frontend.
2. Basic unit test cases with majority coverage is defined. Integration tests are not included.
3. Github Codespaces is ran for this repository but with the default devcontainer image.

## Project Structure

```
root/
├── backend/
│ ├── geo_notes/ # Django project root
│ │ ├── init.py
│ │ ├── settings.py
│ │ ├── urls.py
│ │ ├── wsgi.py
│ │ └── ...
│ ├── accounts/ # Django app for user accounts
│ │ ├── init.py
│ │ ├── admin.py
│ │ ├── apps.py
│ │ ├── models.py
│ │ ├── serializers.py
│ │ ├── urls.py
│ │ ├── views.py
│ │ └── ...
│ ├── pois/ # Django app for points of interest
│ │ ├── init.py
│ │ ├── admin.py
│ │ ├── apps.py
│ │ ├── models.py
│ │ ├── serializers.py
│ │ ├── urls.py
│ │ ├── views.py
│ │ └── ...
│ ├── manage.py
│ ├── requirements.txt
└─├── .env
│ └── ...
├── frontend/
│ ├── public/
│ ├── src/
│ │ ├── components/
│ │ │ ├── LoginComponent.js
│ │ │ ├── RegisterComponent.js
│ │ │ ├── MapComponent.js
│ │ │ ├── LandingPageComponent.js
│ │ │ └── ...
│ │ ├── App.js
│ │ ├── index.js
│ │ └── ...
│ ├── package.json
│ ├── package-lock.json
│ ├── .env
│ └── ...
├── Dockerfile
├── docker-compose.yml
├── README.md
```


## Prerequisites

Ensure you have the following installed on your system:

- Docker
- Docker Compose

## Installation

1. Clone the repository:

    ```sh
    git clone git@github.com:palashsarkar18/geo-notes-application.git
    cd geo_notes
    ```

2. Set up environment variables:

    Create a .env file in the backend and frontend directories with the required environment variables. Take a look
    at the `.env.example` files in the backend and frontend directories.

## Running the Application

1. Start the Docker containers from the root directory:

    ```sh
    docker-compose up --build
    ```

2. The backend will be accessible at `http://localhost:8000` and the frontend at `http://localhost:3000`.

## Environment Variables

- **Root `.env`**:

    ```env
    SECRET_KEY=<your_secret_key>
    DEBUG=True
    POSTGRES_DB=<your_geo_notes_db_name>
    POSTGRES_USER=postgres
    POSTGRES_PASSWORD=<your_postgres_password>
    POSTGRES_SERVER=db
    POSTGRES_PORT=5432
    ```

- **Frontend `.env`** (located in `frontend/.env`):

    ```env
    REACT_APP_API_URL=http://localhost:8000/api
    ```

## Usage

- **Landing Page**: Visit `http://localhost:3000` to access the landing page with options to log in or register.
- **Login/Register**: Use the provided forms to authenticate or create a new account.
- **Map**: After logging in, you will be redirected to the map page where you can view and manage POIs.

## API Endpoints

**Auth Endpoints**
* POST /api/accounts/register/ - Register a new user
* POST /api/accounts/login/ - Login a user
* POST /api/accounts/logout/ - Logout a user
* GET /api/accounts/csrf-token/ - Get CSRF token
* Points of Interest Endpoints
* GET /api/pois/ - List all points of interest
* POST /api/pois/ - Create a new point of interest
* GET /api/pois/<int:id>/ - Retrieve a point of interest
* PUT /api/pois/<int:id>/ - Update a point of interest
* PATCH /api/pois/<int:id>/ - Partially update a point of interest
* DELETE /api/pois/<int:id>/ - Delete a point of interest

## Test
Run the tests using Docker:
```
docker-compose run tests
```
The coverage report will be displayed in the terminal after the tests are executed.

```
2024-06-16 00:05:35 ---------- coverage: platform linux, python 3.12.4-final-0 -----------
2024-06-16 00:05:35 Name                                    Stmts   Miss  Cover   Missing
2024-06-16 00:05:35 ---------------------------------------------------------------------
2024-06-16 00:05:35 accounts/__init__.py                        0      0   100%
2024-06-16 00:05:35 accounts/apps.py                            4      0   100%
2024-06-16 00:05:35 accounts/migrations/0001_initial.py         7      0   100%
2024-06-16 00:05:35 accounts/migrations/__init__.py             0      0   100%
2024-06-16 00:05:35 accounts/models.py                          6      1    83%   12
2024-06-16 00:05:35 accounts/serializers.py                    11      0   100%
2024-06-16 00:05:35 accounts/tests/test_accounts_views.py      29      0   100%
2024-06-16 00:05:35 accounts/urls.py                            3      3     0%   1-4
2024-06-16 00:05:35 accounts/views.py                          46      3    93%   23, 55, 78
2024-06-16 00:05:35 ---------------------------------------------------------------------
2024-06-16 00:05:35 TOTAL                                     106      7    93%
```