# **FitnessHub**

FitnessHub is a comprehensive, full-stack personal wellness planner. It provides a secure, robust, and scalable backend API for a modern, single-page frontend application. It moves beyond simple static logs by providing a dynamic and secure backend, allowing authenticated users to manage and track their fitness journey in granular detail.

The "why" of this project is to provide a single, reliable platform for users to manage their fitness journey. It connects user authentication with deep, relational data, tracking not just that a user worked out, but the specific sets, reps, and weight for every exercise. It also provides a detailed, date-based diet planner to log meals and track caloric intake against a user-defined goal.

The backend is built with Django and Django REST Framework, containerized with Docker, and connected to a PostgreSQL database. The frontend is a modern, responsive static HTML/JavaScript file that provides a dynamic, app-like experience without requiring a complex JavaScript framework.

Installation
This project is designed to be run with Docker and Docker Compose.

# 1. Clone the repository
git clone https://github.com/engrawaiszafar/FitnessHub.git

`cd fitnesshub`

# 2. Build and start the containers in the background
This will build the 'app' image and start 'app' and 'db' services.

`docker-compose up --build -d`

# 3. Run database migrations
This applies the database schema (models) to the PostgreSQL container.

_`docker-compose exec app python manage.py migrate`_

# 4. (Optional) Create a superuser to access the Django admin
This admin panel is at _http://127.0.0.1:8000/admin/_

docker-compose exec app python manage.py createsuperuser

### Getting Started

The project is split into two parts: 

* the backend API

* the frontend HTML file.

### 1. Running the Backend API

To run the backend, simply use Docker Compose:

#### Start all services (if they are not already running)
`docker-compose up`

The API will be running at http://127.0.0.1:8000/api/

### 2. Running the Frontend Application

The frontend is a single, self-contained HTML file (e.g., Weekly Workout Planner.html). This file is not served by the backend.

To run the app, simply open the .html file directly in your web browser (e.g., by double-clicking it).

The JavaScript in the file is already configured to connect to your local API at http://127.0.0.1:8000. You can create an account, log in, and use all the features of the application.

# License

The MIT License (MIT)

Copyright (c) 2025 [Muhammad Awais Zafar]

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.