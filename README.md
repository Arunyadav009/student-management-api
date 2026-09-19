
# Student Management REST API

A backend REST API built with **Python, FastAPI, SQLAlchemy, PostgreSQL, Pydantic, and Alembic** for managing students and departments.

This project was built as a learning-focused backend project to understand REST APIs, database integration, CRUD operations, relationships, validation, pagination, error handling, and database migrations.

## Features

* Student CRUD operations
* Department CRUD operations
* PostgreSQL database integration
* SQLAlchemy ORM
* Pydantic request and response validation
* Student–Department relationship
* Unique email validation
* Course and minimum-age filtering
* Pagination
* Partial student updates
* Proper HTTP status codes
* Database error handling
* Alembic database migrations
* JWT authentication — currently being implemented

## Tech Stack

* **Python**
* **FastAPI**
* **Pydantic**
* **SQLAlchemy**
* **PostgreSQL**
* **Alembic**
* **psycopg**
* **python-dotenv**
* **Git & GitHub**

## Project Structure

```text
student_Crud_api/
│
├── alembic/
│   ├── versions/
│   └── env.py
│
├── .env
├── .gitignore
├── alembic.ini
├── database.py
├── main.py
├── models.py
├── schemas.py
├── README.md
└── student.db
```

> `.env`, `student.db`, `.venv`, and Python cache files should not be committed to GitHub.

## API Endpoints

### Students

| Method | Endpoint                   | Description                                |
| ------ | -------------------------- | ------------------------------------------ |
| POST   | `/students`              | Create a student                           |
| GET    | `/students`              | Get students with filtering and pagination |
| GET    | `/students/{student_id}` | Get a student by ID                        |
| PUT    | `/students/{student_id}` | Partially update a student                 |
| DELETE | `/students/{student_id}` | Delete a student                           |

### Departments

| Method | Endpoint                         | Description            |
| ------ | -------------------------------- | ---------------------- |
| POST   | `/departments`                 | Create a department    |
| GET    | `/departments`                 | Get all departments    |
| GET    | `/departments/{department_id}` | Get a department by ID |

## Database Design

The project uses two main tables:

### Department

* `id`
* `name`

### Student

* `id`
* `name`
* `age`
* `course`
* `email`
* `department_id`

A department can have multiple students.

```text
Department
    │
    │ 1
    │
    └──────────< Student
                    │
                    └── department_id
```

The relationship is implemented using a SQLAlchemy `ForeignKey` and `relationship()`.

## Validation

The API uses Pydantic to validate incoming data.

Examples:

* Student age must be greater than `0`
* Student age cannot exceed `100`
* Email must be a valid email format
* Department ID must reference an existing department
* Student email must be unique

Invalid request data results in appropriate HTTP errors such as `422`.

## Filtering and Pagination

The student listing endpoint supports:

* Course filtering
* Minimum age filtering
* Page number
* Page size

Example:

```text
GET /students?course=CSE&min_age=18&page=1&limit=10
```

The response includes:

* Current page
* Page limit
* Total number of matching students
* Student records

## Error Handling

The API handles common database and request errors, including:

* `404` — Resource not found
* `400` — Invalid database-related request
* `409` — Duplicate student email
* `422` — Request validation error
* `204` — Successful deletion with no response body
* `201` — Successfully created resource

Database transactions are handled using SQLAlchemy sessions with `commit()` and `rollback()` where appropriate.

## Database Migrations

**Alembic** is used to manage database schema changes.

Instead of creating database tables automatically every time the application starts, schema changes are tracked through migration files.

Example:

```bash
alembic upgrade head
```

This applies the latest database migrations.

## Authentication

JWT authentication is currently being implemented.

The planned authentication flow is:

```text
Register
   ↓
Hash Password
   ↓
Login
   ↓
Verify Credentials
   ↓
Generate JWT
   ↓
Client Receives Token
   ↓
Client Sends Token With Protected Requests
   ↓
Server Verifies Token
```

## Running the Project

### 1. Clone the repository

```bash
git clone https://github.com/Arunyadav009/student-management-api.git
cd student-management-api
```

### 2. Create and activate a virtual environment

```bash
python -m venv .venv
```

Windows:

```bash
.venv\Scripts\activate
```

### 3. Install dependencies

The project currently does not include a dependency file, so install the required packages manually:

```bash
pip install fastapi uvicorn sqlalchemy psycopg alembic python-dotenv pydantic email-validator
```

### 4. Configure environment variables

Create a `.env` file and add your PostgreSQL database URL:

```env
DATABASE_URL=your_database_url
```

Do not commit `.env` or database credentials to GitHub.

### 5. Run database migrations

```bash
alembic upgrade head
```

### 6. Start the FastAPI server

```bash
uvicorn main:app --reload
```

The API will be available locally at:

```text
http://127.0.0.1:8000
```

Interactive API documentation is available at:

```text
http://127.0.0.1:8000/docs
```

## Future Improvements

* Complete JWT authentication
* Add password hashing
* Add automated tests with pytest
* Dockerize the application
* Add more advanced filtering and sorting
* Improve test coverage
* Add role-based authorization

## Author

**Arun Yadav**

GitHub: Arunyadav009
