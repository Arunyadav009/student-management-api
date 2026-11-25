
# Student Management REST API

A backend REST API built using **Python, FastAPI, PostgreSQL, SQLAlchemy, and Pydantic**, featuring JWT authentication, role-based access control, database migrations, automated testing, and Docker support.

The project demonstrates practical backend development concepts, including REST API design, database relationships, CRUD operations, validation, authentication, authorization, error handling, and containerization.

## Features

- Student CRUD operations
- Department management
- PostgreSQL database integration
- SQLAlchemy ORM
- Pydantic request and response validation
- Student–Department relationship
- Unique email constraint
- Course and minimum-age filtering
- Pagination
- Partial student updates
- JWT-based authentication
- Password hashing
- Role-based access control (Admin/User)
- Protected API endpoints
- Alembic database migrations
- Automated tests using pytest
- Docker and Docker Compose support

## Tech Stack

| Technology   | Purpose                      |
| ------------ | ---------------------------- |
| Python       | Backend programming          |
| FastAPI      | REST API framework           |
| PostgreSQL   | Relational database          |
| SQLAlchemy   | ORM and database operations  |
| Pydantic     | Data validation              |
| Alembic      | Database migrations          |
| PyJWT        | JWT authentication           |
| pwdlib       | Password hashing             |
| pytest       | Automated testing            |
| Docker       | Application containerization |
| Git & GitHub | Version control              |

## Project Structure

```text
student-management-api/
│
├── alembic/
│   └── versions/
│
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   └── test_basic.py
│
├── .dockerignore
├── .gitignore
├── alembic.ini
├── compose.yaml
├── database.py
├── Dockerfile
├── main.py
├── models.py
├── schemas.py
├── security.py
├── requirements.txt
└── README.md
```

## Database Design

The application uses three main database tables:

### Department

- `id`
- `name`

### Student

- `id`
- `name`
- `age`
- `course`
- `email`
- `department_id`

### User

- `id`
- `name`
- `email`
- `password_hash`
- `role`

A department can have multiple students. The relationship is implemented using SQLAlchemy foreign keys and relationships.

## API Endpoints

### Authentication

| Method | Endpoint      | Description                  | Access |
| ------ | ------------- | ---------------------------- | ------ |
| POST   | `/register` | Register a new user          | Public |
| POST   | `/login`    | Authenticate and receive JWT | Public |

### Students

| Method | Endpoint                   | Description                               | Access        |
| ------ | -------------------------- | ----------------------------------------- | ------------- |
| POST   | `/students`              | Create a student                          | Admin         |
| GET    | `/students`              | List students with filters and pagination | Authenticated |
| GET    | `/students/{student_id}` | Get a student by ID                       | Authenticated |
| PUT    | `/students/{student_id}` | Update a student                          | Admin         |
| DELETE | `/students/{student_id}` | Delete a student                          | Admin         |

### Departments

| Method | Endpoint                         | Description            | Access        |
| ------ | -------------------------------- | ---------------------- | ------------- |
| POST   | `/departments`                 | Create a department    | Admin         |
| GET    | `/departments`                 | List departments       | Authenticated |
| GET    | `/departments/{department_id}` | Get a department by ID | Authenticated |

## Authentication and Authorization

The application uses JWT-based authentication.

Authentication flow:

1. A user registers with their name, email, and password.
2. The password is securely hashed before being stored.
3. The user logs in with their credentials.
4. The server verifies the credentials.
5. A JWT access token is generated.
6. The client sends the token with protected API requests.

Authorization is implemented using role-based access control.

Two roles are supported:

- **User:** Can access protected read-only endpoints.
- **Admin:** Can access read endpoints and perform student and department write operations.

Newly registered users receive the `user` role by default. Public registration does not allow users to assign themselves the admin role.

Protected requests use the following header:

```http
Authorization: Bearer YOUR_ACCESS_TOKEN
```

## Filtering and Pagination

The student listing endpoint supports:

- Course filtering
- Minimum age filtering
- Page number
- Page size

Example:

```http
GET /students?course=CSE&min_age=18&page=1&limit=10
```

## Validation and Error Handling

Pydantic validates incoming request data.

Examples:

- Student age must be greater than zero.
- Student age cannot exceed 100.
- Email must have a valid format.
- Department ID must reference an existing department.
- Student email must be unique.

The API uses appropriate HTTP status codes, including:

| Status | Meaning                            |
| ------ | ---------------------------------- |
| 200    | Successful request                 |
| 201    | Resource created                   |
| 204    | Successful deletion                |
| 400    | Invalid request                    |
| 401    | Authentication required or invalid |
| 403    | Insufficient permissions           |
| 404    | Resource not found                 |
| 409    | Duplicate student email            |
| 422    | Request validation error           |

## Database Migrations

Alembic manages database schema changes.

The migration history includes:

- Initial students table
- Unique email constraint
- Departments and student relationship
- Users table
- User role column

Apply migrations using:

```bash
alembic upgrade head
```

## Running with Docker

### Prerequisites

- Git
- Docker Desktop or Docker Engine with Docker Compose

### 1. Clone the repository

```bash
git clone https://github.com/Arunyadav009/student-management-api.git
cd student-management-api
```

### 2. Configure environment variables

Create a `.env` file in the project root:

```env
POSTGRES_PASSWORD=your_secure_database_password
SECRET_KEY=your_secret_key
```

Generate a secure JWT secret key using Python:

```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

Use the generated value for `SECRET_KEY`.

### 3. Build and start the containers

```bash
docker compose up --build -d
```

This starts the FastAPI application and PostgreSQL database.

### 4. Apply database migrations

```bash
docker compose exec api alembic upgrade head
```

### 5. Verify running containers

```bash
docker compose ps
```

### 6. Access the application

API:

```text
http://localhost:8000
```

Interactive Swagger documentation:

```text
http://localhost:8000/docs
```

Stop the containers:

```bash
docker compose down
```

To stop containers and remove the PostgreSQL data volume:

```bash
docker compose down -v
```

**Warning:** The second command permanently deletes the database data stored in the Compose volume.

## Running Locally

### 1. Create a virtual environment

```bash
python -m venv .venv
```

Activate it on Windows:

```powershell
.venv\Scripts\activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure environment variables

Create a `.env` file with your PostgreSQL connection string and JWT secret:

```env
DATABASE_URL=postgresql+psycopg://username:password@localhost:5432/student_management
TEST_DATABASE_URL=postgresql+psycopg://username:password@localhost:5432/student_management_test
SECRET_KEY=your_secret_key
```

The test database must be created separately. Keep it separate from your development or production database because the test fixtures create and drop database tables.

### 4. Apply migrations

```bash
alembic upgrade head
```

### 5. Start the application

```bash
uvicorn main:app --reload
```

The application will run at:

```text
http://127.0.0.1:8000
```

## Running Automated Tests

Run the test suite using:

```bash
pytest -v
```

The tests cover API functionality and role-based access control.

Latest verified result: **23 tests passed.**

## Security and Configuration

- Database credentials and JWT secrets are stored in environment variables.
- `.env` is excluded from Git.
- Passwords are stored as hashes rather than plaintext.
- JWT tokens are validated before protected operations.
- Public registration cannot assign administrative privileges.
- Administrative operations require the admin role.

## Author

**Arun Yadav**

GitHub: [Arunyadav009](https://github.com/Arunyadav009)

Project Repository: [Student Management REST API](https://github.com/Arunyadav009/student-management-api)
