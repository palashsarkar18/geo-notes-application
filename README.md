# Geo Notes

Geo Notes is a full-stack web application that allows users to register, log in, and manage points of interest (POIs) on a map. The backend is built with Django and the frontend with React. The project is containerized using Docker.

## Table of Contents

- [Geo Notes](#geo-notes)
  - [Table of Contents](#table-of-contents)
  - [Project Structure](#project-structure)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Running the Application](#running-the-application)
  - [Environment Variables](#environment-variables)
  - [Usage](#usage)
  - [API Endpoints](#api-endpoints)
    - [Test](#test)
  - [Contributing](#contributing)
  - [TODO](#todo)

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
│ │ │ ├── Login.js
│ │ │ ├── Register.js
│ │ │ ├── MapComponent.js
│ │ │ ├── LandingPage.js
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
    git clone https://github.com/your-username/geo_notes.git
    cd geo_notes
    ```

2. Create a `.env` file in the root directory with the following content:

    ```env
    DATABASE_NAME=geo_notes_db
    DATABASE_USER=geo_user
    DATABASE_PASSWORD=geo_password
    DATABASE_HOST=db
    DATABASE_PORT=5432
    ```

3. Navigate to the `frontend` directory and install the dependencies:

    ```sh
    cd frontend
    npm install
    ```

## Running the Application

1. Navigate back to the root directory and start the Docker containers:

    ```sh
    cd ..
    docker-compose up --build
    ```

2. The backend will be accessible at `http://localhost:8000` and the frontend at `http://localhost:3000`.

## Environment Variables

- **Root `.env`**:

    ```env
    DATABASE_NAME=geo_notes_db
    DATABASE_USER=geo_user
    DATABASE_PASSWORD=geo_password
    DATABASE_HOST=db
    DATABASE_PORT=5432
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

- **CSRF Token**: `GET /api/csrf-token/`
- **Register**: `POST /api/accounts/register/`
- **Login**: `POST /api/accounts/login/`
- **Logout**: `POST /api/accounts/logout/`
- **POIs**: `GET /api/pois/`

### Test
```
pytest --cov=accounts --cov=geo_notes --cov=pois --cov-report=term-missing
```

## Contributing

Contributions are welcome! Please follow these steps to contribute:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make your changes.
4. Commit your changes (`git commit -am 'Add new feature'`).
5. Push to the branch (`git push origin feature-branch`).
6. Create a new Pull Request.

## TODO

* Add create and update time on UI?
* Add tooltip on the UI with the option for edit/delete
* GraphQL?
* Github codespaces
* Add comments as docstring
* Type hint?
* Define scope
* Check if docker compose works without the build folder?
* Check the latitude longiture limitation. The values should be in the range.