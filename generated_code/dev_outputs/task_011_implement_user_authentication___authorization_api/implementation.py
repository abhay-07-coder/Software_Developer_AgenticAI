An expert-level, production-grade implementation for the User Authentication & Authorization API is provided below. This solution uses Python with FastAPI, PostgreSQL, SQLAlchemy, and JWT for a robust and scalable service.

## Architecture & Design

This implementation follows a clean, modular architecture designed for maintainability and scalability, suitable for a microservices environment.

-   **Layered Architecture**: The code is organized into distinct layers:
    1.  **API Layer (`app/api`)**: Handles HTTP requests and responses. It contains endpoint definitions (`endpoints`) and data transfer objects (`schemas`).
    2.  **Service/CRUD Layer (`app/crud`)**: Encapsulates the business logic for interacting with the database models. This decouples the API layer from the data access layer.
    3.  **Data Layer (`app/db`)**: Defines the database models (`models`), session management (`session`), and the base for declarative models (`base`).
    4.  **Core Logic (`app/core`)**: Contains cross-cutting concerns like configuration management (`config`) and security utilities (`security`).

-   **Dependency Injection**: FastAPI's dependency injection system is heavily utilized (`app/api/deps.py`) to manage database sessions and user authentication. This improves testability and adheres to the Inversion of Control principle.

-   **Configuration Management**: A Pydantic `Settings` class (`app/core/config.py`) loads configuration from environment variables, providing a single source of truth and making the application environment-agnostic.

-   **Security-First Design**:
    -   **Passwords**: Never stored in plaintext. `passlib` with the `bcrypt` algorithm is used for strong, salted hashing.
    -   **Authentication**: Stateless JWTs are used for authentication, which is ideal for microservices.
    -   **Authorization**: Protected endpoints verify the JWT and can be extended to check user roles or permissions.
    -   **Logout**: A simple in-memory token blocklist is implemented to demonstrate server-side token invalidation. For production at scale, this should be replaced with a distributed cache like Redis.

## Setup Instructions

1.  **Prerequisites**:
    -   Docker and Docker Compose must be installed.
    -   A `.env` file must be created in the project root.

2.  **Create Environment File**:
    -   Create a file named `.env` in the root of the project directory.
    -   Copy the contents of `env.example` into `.env` and adjust the values if necessary. The provided defaults are suitable for local development.

3.  **Build and Run the Application**:
    -   Open a terminal in the project root.
    -   Run the following command to build the containers and start the services (API and PostgreSQL database):
        ```bash
        docker-compose up --build
        ```
    -   The API will be available at `http://localhost:8000`.

4.  **Run Database Migrations**:
    -   After the containers are running, open a new terminal window.
    -   Execute the following command to apply the initial database schema migrations using Alembic:
        ```bash
        docker-compose exec app alembic upgrade head
        ```
    -   This command creates the `users` table in the PostgreSQL database.

5.  **Access API Documentation**:
    -   Once the application is running, navigate to `http://localhost:8000/docs` in your browser to view the interactive Swagger UI documentation.

6.  **Run Tests**:
    -   To execute the test suite, run the following command:
        ```bash
        docker-compose exec app pytest
        ```

## Project Structure

```
/user-auth-service
├── app/
│   ├── __init__.py
│   ├── api/
│   │   ├── __init__.py
│   │   ├── deps.py
│   │   └── v1/
│   │       ├── __init__.py
│   │       ├── endpoints/
│   │       │   ├── __init__.py
│   │       │   └── auth.py
│   │       └── schemas.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py
│   │   └── security.py
│   ├── crud/
│   │   ├── __init__.py
│   │   └── crud_user.py
│   ├── db/
│   │   ├── __init__.py
│   │   ├── base.py
│   │   ├── session.py
│   │   └── models/
│   │       ├── __init__.py
│   │       └── user.py
│   ├── main.py
│   └── tests/
│       ├── __init__.py
│       ├── conftest.py
│       └── api/
│           └── v1/
│               └── test_auth.py
├── alembic/
│   ├── versions/
│   │   └── 20231027_initial_migration.py
│   ├── env.py
│   └── script.py.mako
├── alembic.ini
├── .env.example
├── .gitignore
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
└── README.md
```

---

## `env.example`

This file serves as a template for the required environment variables.

```ini
# env.example
# Copy this file to .env and fill in the values.

# PostgreSQL Database Configuration
POSTGRES_SERVER=db
POSTGRES_USER=appuser
POSTGRES_PASSWORD=securepassword
POSTGRES_DB=appdb
DATABASE_URL=postgresql://appuser:securepassword@db/appdb

# JWT Settings
# To generate a good secret key, run: openssl rand -hex 32
SECRET_KEY=09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7
ACCESS_TOKEN_EXPIRE_MINUTES=30
ALGORITHM=HS256

# Application Settings
PROJECT_NAME="User Authentication Service"
API_V1_STR="/api/v1"
```

## `requirements.txt`

List of all Python dependencies for the project.

```text
# requirements.txt
# Core FastAPI and server
fastapi==0.104.0
uvicorn[standard]==0.23.2

# Database
sqlalchemy==2.0.22
psycopg2-binary==2.9.9
alembic==1.12.0

# Pydantic for settings management
pydantic-settings==2.0.3

# Security
passlib[bcrypt]==1.7.4
python-jose[cryptography]==3.3.0
python-multipart==0.0.6 # For OAuth2PasswordRequestForm

# Testing
pytest==7.4.2
httpx==0.25.0
```

## `Dockerfile`

A multi-stage Dockerfile for building a lean, production-ready container image.

```dockerfile
# Dockerfile

# --- Build Stage ---
FROM python:3.11-slim as builder

# Set working directory
WORKDIR /usr/src/app

# Set environment variables to prevent writing .pyc files and to buffer output
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install system dependencies required for building some python packages
RUN apt-get update && \
    apt-get install -y --no-install-recommends build-essential libpq-dev && \
    rm -rf /var/lib/apt/lists/*

# Install poetry for dependency management
# Using poetry is a best practice, but for simplicity here we use pip with requirements.txt
COPY requirements.txt .
RUN pip wheel --no-cache-dir --wheel-dir /usr/src/app/wheels -r requirements.txt


# --- Final Stage ---
FROM python:3.11-slim

# Create a non-root user
RUN addgroup --system app && adduser --system --group app

# Set working directory
WORKDIR /home/app

# Install dependencies from wheel files
COPY --from=builder /usr/src/app/wheels /wheels
COPY --from=builder /usr/src/app/requirements.txt .
RUN pip install --no-cache /wheels/*

# Copy application code
COPY ./app /home/app/app
COPY ./alembic /home/app/alembic
COPY ./alembic.ini /home/app/alembic.ini

# Change ownership to the non-root user
RUN chown -R app:app /home/app

# Switch to the non-root user
USER app

# Expose the port the app runs on
EXPOSE 8000

# Command to run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## `docker-compose.yml`

Orchestrates the API service and the PostgreSQL database for local development.

```yaml
# docker-compose.yml
version: '3.8'

services:
  db:
    image: postgres:15-alpine
    volumes:
      - postgres_data:/var/lib/postgresql/data/
    env_file:
      - .env
    ports:
      - "5432:5432"
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ${POSTGRES_USER} -d ${POSTGRES_DB}"]
      interval: 10s
      timeout: 5s
      retries: 5

  app:
    build: .
    env_file:
      - .env
    ports:
      - "8000:8000"
    depends_on:
      db:
        condition: service_healthy
    command: uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

volumes:
  postgres_data:
```

## `alembic.ini`

Configuration file for Alembic database migrations.

```ini
# alembic.ini
[alembic]
script_location = alembic
sqlalchemy.url = driver://user:pass@localhost/dbname

[loggers]
keys = root,sqlalchemy,alembic

[handlers]
keys = console

[formatters]
keys = generic

[logger_root]
level = WARN
handlers = console
qualname =

[logger_sqlalchemy]
level = WARN
handlers =
qualname = sqlalchemy.engine

[logger_alembic]
level = INFO
handlers =
qualname = alembic

[handler_console]
class = StreamHandler
args = (sys.stderr,)
level = NOTSET
formatter = generic

[formatter_generic]
format = %(levelname)-5.5s [%(name)s] %(message)s
datefmt = %H:%M:%S
```

## `alembic/env.py`

Alembic environment setup, configured to use the application's models and database URL.

```python
# alembic/env.py
import os
from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
from app.db.base import Base  # noqa
from app.db.models.user import User # noqa
target_metadata = Base.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.

def get_url():
    return os.getenv("DATABASE_URL")

def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = get_url()
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    configuration = config.get_section(config.config_ini_section)
    configuration["sqlalchemy.url"] = get_url()
    connectable = engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
```

## `alembic/versions/20231027_initial_migration.py`

The first migration script to create the `users` table.

```python
# alembic/versions/20231027_initial_migration.py
"""initial migration

Revision ID: 2b18b7b3a9c7
Revises: 
Create Date: 2023-10-27 10:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2b18b7b3a9c7'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('hashed_password', sa.String(), nullable=False),
    sa.Column('is_active', sa.Boolean(), server_default='true', nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    op.create_index(op.f('ix_users_id'), 'users', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_users_id'), table_name='users')
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_table('users')
    # ### end Alembic commands ###
```

## `app/main.py`

The main entry point for the FastAPI application.

```python
# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.endpoints import auth
from app.core.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Set all CORS enabled origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, restrict this to your frontend's domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health check endpoint
@app.get("/health", tags=["Health Check"])
def health_check():
    """
    Health check endpoint to verify service is running.
    """
    return {"status": "ok"}

# Include the authentication router
app.include_router(auth.router, prefix=settings.API_V1_STR, tags=["Authentication"])
```

## `app/core/config.py`

Pydantic-based settings management.

```python
# app/core/config.py
from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    PROJECT_NAME: str = "User Authentication Service"
    API_V1_STR: str = "/api/v1"

    # Database
    POSTGRES_SERVER: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    DATABASE_URL: Optional[str] = None

    # JWT
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    ALGORITHM: str = "HS256"

    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
```

## `app/core/security.py`

Handles password hashing, JWT creation, and token verification.

```python
# app/core/security.py
from datetime import datetime, timedelta
from typing import Any, Union

from jose import jwt
from passlib.context import CryptContext

from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# A simple in-memory set to store invalidated tokens.
# In a production/distributed environment, use a persistent store like Redis.
TOKEN_BLACKLIST: set = set()

ALGORITHM = settings.ALGORITHM

def create_access_token(
    subject: Union[str, Any], expires_delta: timedelta = None
) -> str:
    """
    Creates a JWT access token.
    """
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifies a plain password against a hashed password.
    """
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """
    Hashes a plain password.
    """
    return pwd_context.hash(password)

def add_token_to_blacklist(token: str) -> None:
    """
    Adds a token to the blacklist.
    """
    TOKEN_BLACKLIST.add(token)

def is_token_blacklisted(token: str) -> bool:
    """
    Checks if a token is in the blacklist.
    """
    return token in TOKEN_BLACKLIST
```

## `app/db/session.py`

Database session and engine setup.

```python
# app/db/session.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

engine = create_engine(settings.DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
```

## `app/db/base.py`

Base class for SQLAlchemy models.

```python
# app/db/base.py
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.declarative import declared_attr

class Base(DeclarativeBase):
    id: any
    __name__: str

    # to generate tablename from classname
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower() + "s"
```

## `app/db/models/user.py`

SQLAlchemy User model definition.

```python
# app/db/models/user.py
from sqlalchemy import Column, Integer, String, Boolean, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base

class User(Base):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, server_default="true", nullable=False)
    
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
```

## `app/crud/crud_user.py`

CRUD functions for the User model.

```python
# app/crud/crud_user.py
from sqlalchemy.orm import Session

from app.db.models.user import User
from app.api.v1.schemas import UserCreate
from app.core.security import get_password_hash

def get_user_by_email(db: Session, *, email: str) -> User | None:
    """
    Retrieves a user by their email address.
    """
    return db.query(User).filter(User.email == email).first()

def create_user(db: Session, *, user_in: UserCreate) -> User:
    """
    Creates a new user in the database.
    """
    hashed_password = get_password_hash(user_in.password)
    db_user = User(
        email=user_in.email,
        hashed_password=hashed_password,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
```

## `app/api/v1/schemas.py`

Pydantic schemas for request/response validation and serialization.

```python
# app/api/v1/schemas.py
from pydantic import BaseModel, EmailStr
from datetime import datetime

# --- Token Schemas ---
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: EmailStr | None = None

# --- User Schemas ---
class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True # Replaces orm_mode = True
```

## `app/api/deps.py`

FastAPI dependencies for database sessions and user authentication.

```python
# app/api/deps.py
from typing import Generator

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from pydantic import ValidationError
from sqlalchemy.orm import Session

from app.core import security
from app.core.config import settings
from app.db.session import SessionLocal
from app.db.models.user import User
from app.crud import crud_user
from app.api.v1 import schemas

reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/login"
)

def get_db() -> Generator:
    """
    Dependency to get a database session.
    """
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

def get_current_user(
    db: Session = Depends(get_db), token: str = Depends(reusable_oauth2)
) -> User:
    """
    Dependency to get the current user from a JWT token.
    """
    if security.is_token_blacklisted(token):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has been revoked (logged out)",
        )
        
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = schemas.TokenData(email=email)
    except (JWTError, ValidationError):
        raise credentials_exception
    
    user = crud_user.get_user_by_email(db, email=token_data.email)
    if user is None:
        raise credentials_exception
    return user

def get_current_active_user(
    current_user: User = Depends(get_current_user),
) -> User:
    """
    Dependency to get the current active user.
    Raises an exception if the user is inactive.
    """
    if not current_user.is_active:
        raise HTTPException(status_code=403, detail="Inactive user")
    return current_user
```

## `app/api/v1/endpoints/auth.py`

API endpoints for registration, login, logout, and profile management.

```python
# app/api/v1/endpoints/auth.py
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.api import deps
from app.api.v1 import schemas
from app.crud import crud_user
from app.core import security
from app.db.models.user import User

router = APIRouter()

@router.post("/register", response_model=schemas.User, status_code=status.HTTP_201_CREATED)
def register_user(
    *,
    db: Session = Depends(deps.get_db),
    user_in: schemas.UserCreate,
) -> Any:
    """
    Create new user.
    """
    user = crud_user.get_user_by_email(db, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this email already exists in the system.",
        )
    user = crud_user.create_user(db=db, user_in=user_in)
    return user

@router.post("/login", response_model=schemas.Token)
def login_for_access_token(
    db: Session = Depends(deps.get_db),
    form_data: OAuth2PasswordRequestForm = Depends()
) -> Any:
    """
    OAuth2 compatible token login, get an access token for future requests.
    """
    user = crud_user.get_user_by_email(db, email=form_data.username)
    if not user or not security.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    
    access_token = security.create_access_token(
        subject=user.email
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
def logout(
    token: str = Depends(deps.reusable_oauth2),
    current_user: User = Depends(deps.get_current_user)
):
    """
    Logout user by invalidating the current token.
    """
    security.add_token_to_blacklist(token)
    return None

@router.get("/me", response_model=schemas.User)
def read_users_me(
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get current user's profile.
    """
    return current_user
```

## `app/tests/conftest.py`

Pytest fixtures for setting up the test environment.

```python
# app/tests/conftest.py
import pytest
from typing import Generator

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.api.deps import get_db
from app.db.base import Base
from app.core.config import settings

# Use a separate test database
TEST_DATABASE_URL = f"{settings.DATABASE_URL}_test"

engine = create_engine(TEST_DATABASE_URL, pool_pre_ping=True)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="session", autouse=True)
def setup_db():
    """
    Create the test database and tables before tests run, and drop them after.
    """
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def db() -> Generator:
    """
    Provides a test database session for each test function.
    """
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    yield session
    session.close()
    transaction.rollback()
    connection.close()

@pytest.fixture(scope="function")
def client(db: Generator) -> Generator:
    """
    Provides a TestClient for making requests to the app.
    """
    def override_get_db():
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    # Clean up dependency override after test
    app.dependency_overrides.clear()
```

## `app/tests/api/v1/test_auth.py`

Integration tests for the authentication API endpoints.

```python
# app/tests/api/v1/test_auth.py
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
import uuid

from app.core.config import settings

def get_random_email():
    return f"test_{uuid.uuid4()}@example.com"

def test_user_registration(client: TestClient, db: Session):
    email = get_random_email()
    password = "a_secure_password"
    data = {"email": email, "password": password}
    response = client.post(f"{settings.API_V1_STR}/register", json=data)
    assert response.status_code == 201
    content = response.json()
    assert content["email"] == email
    assert "id" in content
    assert "hashed_password" not in content

def test_duplicate_user_registration(client: TestClient, db: Session):
    email = get_random_email()
    password = "a_secure_password"
    data = {"email": email, "password": password}
    # First registration should succeed
    response1 = client.post(f"{settings.API_V1_STR}/register", json=data)
    assert response1.status_code == 201
    # Second registration with the same email should fail
    response2 = client.post(f"{settings.API_V1_STR}/register", json=data)
    assert response2.status_code == 400
    assert "already exists" in response2.json()["detail"]

def test_user_login(client: TestClient, db: Session):
    email = get_random_email()
    password = "a_secure_password"
    # Register user first
    client.post(f"{settings.API_V1_STR}/register", json={"email": email, "password": password})
    
    # Attempt login
    login_data = {"username": email, "password": password}
    response = client.post(f"{settings.API_V1_STR}/login", data=login_data)
    assert response.status_code == 200
    content = response.json()
    assert "access_token" in content
    assert content["token_type"] == "bearer"

def test_user_login_wrong_password(client: TestClient, db: Session):
    email = get_random_email()
    password = "a_secure_password"
    client.post(f"{settings.API_V1_STR}/register", json={"email": email, "password": password})
    
    login_data = {"username": email, "password": "wrong_password"}
    response = client.post(f"{settings.API_V1_STR}/login", data=login_data)
    assert response.status_code == 401
    assert "Incorrect email or password" in response.json()["detail"]

def test_get_me_unauthenticated(client: TestClient):
    response = client.get(f"{settings.API_V1_STR}/me")
    assert response.status_code == 401
    assert "Not authenticated" in response.json()["detail"]

def test_get_me_authenticated(client: TestClient, db: Session):
    email = get_random_email()
    password = "a_secure_password"
    client.post(f"{settings.API_V1_STR}/register", json={"email": email, "password": password})
    
    login_data = {"username": email, "password": password}
    login_response = client.post(f"{settings.API_V1_STR}/login", data=login_data)
    token = login_response.json()["access_token"]
    
    headers = {"Authorization": f"Bearer {token}"}
    me_response = client.get(f"{settings.API_V1_STR}/me", headers=headers)
    assert me_response.status_code == 200
    content = me_response.json()
    assert content["email"] == email
    assert content["is_active"] is True

def test_logout(client: TestClient, db: Session):
    email = get_random_email()
    password = "a_secure_password"
    client.post(f"{settings.API_V1_STR}/register", json={"email": email, "password": password})
    
    login_data = {"username": email, "password": password}
    login_response = client.post(f"{settings.API_V1_STR}/login", data=login_data)
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Logout
    logout_response = client.post(f"{settings.API_V1_STR}/logout", headers=headers)
    assert logout_response.status_code == 204

    # Try to access a protected route with the logged-out token
    me_response = client.get(f"{settings.API_V1_STR}/me", headers=headers)
    assert me_response.status_code == 401
    assert "Token has been revoked" in me_response.json()["detail"]
```
✅ Streaming completed.