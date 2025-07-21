An architectural overview of the Shopping Cart API microservice.

## Architecture & Design

This solution implements a self-contained Shopping Cart microservice using a layered architecture, which promotes separation of concerns, maintainability, and scalability.

### 1. Layered Architecture

The service is structured into the following distinct layers:

-   **API Layer (`api/`)**: This is the entry point of the application, responsible for handling HTTP requests. It uses FastAPI routers to define endpoints. Its primary role is to parse incoming requests, validate them using Pydantic schemas, and delegate the business logic to the Service Layer. It depends on the Service Layer and Security Layer (for user authentication).
-   **Service Layer (`services/`)**: This layer contains the core business logic. For example, the `CartService` orchestrates the process of adding an item to a cart. It interacts with the CRUD layer to access the database and with other services (like a caching service) to perform its tasks. It's responsible for calculations (e.g., cart totals), validations (e.g., stock availability), and orchestrating data persistence.
-   **CRUD Layer (`crud/`)**: This layer abstracts the database interactions. It provides a simple, reusable interface for Create, Read, Update, and Delete operations on the database models. It is directly used by the Service Layer and is the only layer that should communicate directly with the database ORM.
-   **Data Layer (`models/`, `schemas/`)**:
    -   `models/`: Defines the database schema using SQLAlchemy ORM models. These models represent the tables in our PostgreSQL database.
    -   `schemas/`: Defines the data contracts for our API using Pydantic. These schemas are used for request validation, response serialization, and ensuring type safety throughout the application.
-   **Core Layer (`core/`)**: This layer holds cross-cutting concerns like application configuration, database session management, and security dependencies (e.g., JWT validation).

### 2. Microservice Communication & Dependencies

This Cart Service is designed to operate within a larger microservices ecosystem.

-   **User Authentication (Dependency `task_011`)**: The service does not manage users directly. It relies on an external Authentication Service to issue JWTs. A security dependency (`get_current_user`) is implemented to validate these tokens on protected endpoints and extract the authenticated user's ID.
-   **Product Catalog (Dependency `task_012`)**: To calculate cart totals and check for product availability, the service needs product information (like price and stock). In this implementation, a local `products` table simulates this external Product Catalog service. In a real-world scenario, the `CartService` would make an API call (e.g., gRPC or REST) to the Product Service to fetch this data.

### 3. Performance & Scalability

-   **Asynchronous Operations**: The entire stack (FastAPI, Starlette, SQLAlchemy with `asyncpg`, `aioredis`) is asynchronous, allowing for high concurrency and efficient handling of I/O-bound operations (database and cache access).
-   **Caching**: Redis is used as a caching layer to reduce database load and improve response times for frequently accessed data, specifically the user's cart view (`GET /cart`). A write-through caching strategy is employed: on any modification to the cart, the cache for that user is invalidated, ensuring data consistency.
-   **Database Optimization**: Proper indexing is defined on foreign keys (`user_id`, `cart_id`, `product_id`) and unique constraints to ensure fast lookups and data integrity.
-   **Containerization**: The application and its dependencies (PostgreSQL, Redis) are containerized using Docker, allowing for consistent environments, horizontal scaling, and easy deployment with orchestrators like Kubernetes.

### 4. Security

-   **Authentication**: All endpoints are protected and require a valid JWT `Bearer` token.
-   **Authorization**: Business logic is strictly scoped to the authenticated user. A user can only access and modify their own cart.
-   **Input Validation**: Pydantic schemas provide robust, automatic validation of all incoming request data, preventing malformed data from reaching the business logic.
-   **Environment-based Secrets**: Sensitive information like database credentials and JWT secrets are managed via environment variables, following the 12-Factor App methodology.

This design results in a robust, secure, and performant microservice that is easy to maintain, test, and scale independently.

## Setup Instructions

1.  **Prerequisites**: Ensure you have `Docker` and `docker-compose` installed on your machine.

2.  **Environment Configuration**: Create a file named `.env` in the project root and populate it with the following content.

    ```ini
    # .env
    # PostgreSQL settings
    POSTGRES_USER=cart_user
    POSTGRES_PASSWORD=strongpassword
    POSTGRES_DB=cart_db
    POSTGRES_SERVER=db
    POSTGRES_PORT=5432
    DATABASE_URL=postgresql+asyncpg://cart_user:strongpassword@db:5432/cart_db

    # Redis settings
    REDIS_HOST=redis
    REDIS_PORT=6379

    # JWT settings
    # In a real production environment, use a much more complex secret,
    # possibly loaded from a secret manager.
    # You can generate a good secret with: openssl rand -hex 32
    JWT_SECRET_KEY=09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7
    JWT_ALGORITHM=HS256
    ACCESS_TOKEN_EXPIRE_MINUTES=30

    # Application settings
    PROJECT_NAME="Shopping Cart Service"
    API_V1_STR="/api/v1"
    ```

3.  **Build and Run the Services**: Open a terminal in the project root and run the following command:

    ```bash
    docker-compose up --build
    ```

    This command will:
    -   Build the Docker image for the FastAPI application.
    -   Start containers for the FastAPI app, PostgreSQL database, and Redis.
    -   The application will be available at `http://localhost:8008`.

4.  **Database Migrations**: The first time you run the application, the `command` in `docker-compose.yml` will automatically apply the database migrations. It will also seed the database with sample users and products.

5.  **API Documentation**: Once the application is running, you can access the interactive API documentation (Swagger UI) at:
    `http://localhost:8008/docs`

## How to Use the API

1.  **Get a JWT Token**:
    -   The service is seeded with two users: `user1@example.com` and `user2@example.com`. Both have the password `string`.
    -   Use the `/api/v1/login/access-token` endpoint (available in the Swagger UI) to get a JWT for one of these users.

2.  **Authorize Requests**:
    -   In the Swagger UI, click the "Authorize" button and enter your token in the format `Bearer <YOUR_TOKEN>`.
    -   Now you can make authenticated requests to the cart endpoints.

3.  **Interact with the Cart**:
    -   **Add an item**: Use `POST /api/v1/cart/items` with a `product_id` (e.g., 1 for "Laptop") and a quantity.
    -   **View your cart**: Use `GET /api/v1/cart`.
    -   **Update an item**: Use `PUT /api/v1/cart/items/{cart_item_id}`. You can get the `cart_item_id` from the response of the "View your cart" endpoint.
    -   **Remove an item**: Use `DELETE /api/v1/cart/items/{cart_item_id}`.

## Project Structure

```
.
├── api
│   ├── __init__.py
│   └── v1
│       ├── __init__.py
│       ├── api.py
│       └── endpoints
│           ├── __init__.py
│           ├── cart.py
│           └── login.py
├── core
│   ├── __init__.py
│   ├── config.py
│   ├── db.py
│   └── security.py
├── crud
│   ├── __init__.py
│   ├── base.py
│   └── crud_cart.py
├── db
│   ├── __init__.py
│   ├── base.py
│   ├── init_db.py
│   ├── migrations
│   │   ├── README
│   │   ├── env.py
│   │   ├── script.py.mako
│   │   └── versions
│   │       └── ..._initial_schema.py
│   └── models
│       ├── __init__.py
│       ├── cart.py
│       ├── product.py
│       └── user.py
├── schemas
│   ├── __init__.py
│   ├── cart.py
│   ├── msg.py
│   ├── product.py
│   ├── token.py
│   └── user.py
├── services
│   ├── __init__.py
│   ├── cache_service.py
│   └── cart_service.py
├── tests
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_cart_api.py
│   └── utils.py
├── .env
├── .gitignore
├── Dockerfile
├── README.md
├── alembic.ini
├── docker-compose.yml
├── main.py
└── requirements.txt
```

---

## Code Artifacts

Below are the complete, production-ready code files for the Shopping Cart API service.

### `Dockerfile`
```dockerfile
# Dockerfile

# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install system dependencies required for psycopg2
RUN apt-get update \
    && apt-get -y install gcc libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose the port the app runs on
EXPOSE 8008

# The command to run the application will be in docker-compose.yml
# This allows for flexibility, e.g., running migrations before starting the app.
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8008"]
```

### `docker-compose.yml`
```yaml
# docker-compose.yml
version: '3.8'

services:
  db:
    image: postgres:15
    container_name: cart_postgres_db
    volumes:
      - postgres_data:/var/lib/postgresql/data/
    environment:
      - POSTGRES_USER=${POSTGRES_USER}
      - POSTGRES_PASSWORD=${POSTGRES_PASSWORD}
      - POSTGRES_DB=${POSTGRES_DB}
    ports:
      - "5433:5432" # Expose on 5433 to avoid conflicts with local postgres
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ${POSTGRES_USER} -d ${POSTGRES_DB}"]
      interval: 5s
      timeout: 5s
      retries: 5

  redis:
    image: redis:7-alpine
    container_name: cart_redis
    ports:
      - "6380:6379" # Expose on 6380 to avoid conflicts
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 5s
      timeout: 5s
      retries: 5

  app:
    build: .
    container_name: cart_api_app
    env_file:
      - .env
    ports:
      - "8008:8008"
    depends_on:
      db:
        condition: service_healthy
      redis:
        condition: service_healthy
    # This command runs migrations and seeds the DB before starting the app server
    command: >
      bash -c "alembic upgrade head &&
      python -m db.init_db &&
      uvicorn main:app --host 0.0.0.0 --port 8008 --reload"
    volumes:
      - .:/app

volumes:
  postgres_data:
```

### `requirements.txt`
```txt
# requirements.txt
fastapi==0.111.0
uvicorn[standard]==0.29.0
sqlalchemy[asyncio]==2.0.29
asyncpg==0.29.0
pydantic==2.7.1
pydantic-settings==2.2.1
alembic==1.13.1
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
python-multipart==0.0.9
aioredis==2.0.1

# Testing
pytest==8.2.0
httpx==0.27.0
pytest-asyncio==0.23.6
```

### `alembic.ini`
```ini
# alembic.ini
[alembic]
script_location = db/migrations
sqlalchemy.url = ${DATABASE_URL}

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

### `main.py`
```python
# main.py
import logging
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from api.v1.api import api_router
from core.config import settings
from services.cache_service import CacheService

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan manager.
    Initializes CacheService on startup and closes it on shutdown.
    """
    logger.info("Application startup: Initializing resources.")
    await CacheService.initialize()
    yield
    await CacheService.close()
    logger.info("Application shutdown: Resources closed.")


app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    lifespan=lifespan
)

# Set all CORS enabled origins
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

# Custom exception handlers
@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={"detail": exc.errors()},
    )

# Health check endpoint
@app.get("/health", tags=["Health Check"])
async def health_check():
    """
    Health check endpoint to verify service is running.
    """
    return {"status": "ok"}


app.include_router(api_router, prefix=settings.API_V1_STR)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8008)
```

### `core/config.py`
```python
# core/config.py
from pydantic import AnyHttpUrl
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List, Union

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", case_sensitive=True)

    PROJECT_NAME: str = "Shopping Cart API"
    API_V1_STR: str = "/api/v1"
    
    # Database settings
    POSTGRES_SERVER: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    DATABASE_URL: str

    # Redis settings
    REDIS_HOST: str
    REDIS_PORT: int

    # JWT settings
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # CORS settings
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []

settings = Settings()
```

### `core/db.py`
```python
# core/db.py
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from core.config import settings

# Create an async engine instance
engine = create_async_engine(settings.DATABASE_URL, pool_pre_ping=True)

# Create a session factory
AsyncSessionFactory = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency to get a database session.
    Yields a session and ensures it's closed after the request.
    """
    async with AsyncSessionFactory() as session:
        yield session
```

### `core/security.py`
```python
# core/security.py
from datetime import datetime, timedelta, timezone
from typing import Any, Union

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession

from core.config import settings
from core.db import get_db
from db.models.user import User
from schemas.token import TokenData
from sqlalchemy.future import select

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/login/access-token")

def create_access_token(subject: Union[str, Any], expires_delta: timedelta = None) -> str:
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    return encoded_jwt

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

async def get_current_user(
    db: AsyncSession = Depends(get_db), token: str = Depends(oauth2_scheme)
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM]
        )
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
        token_data = TokenData(user_id=int(user_id))
    except (JWTError, ValueError):
        raise credentials_exception
    
    result = await db.execute(select(User).where(User.id == token_data.user_id))
    user = result.scalar_one_or_none()
    
    if user is None:
        raise credentials_exception
    return user
```

### `db/base.py`
```python
# db/base.py
from db.models.cart import Cart, CartItem
from db.models.product import Product
from db.models.user import User
from db.base_class import Base
```

### `db/base_class.py`
```python
# db/base_class.py
from typing import Any
from sqlalchemy.ext.declarative import as_declarative, declared_attr

@as_declarative()
class Base:
    id: Any
    __name__: str

    # to generate tablename from classname
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower() + "s"
```

### `db/init_db.py`
```python
# db/init_db.py
import logging
from sqlalchemy.ext.asyncio import AsyncSession
from core.db import AsyncSessionFactory
from core.security import get_password_hash
from db.models.user import User
from db.models.product import Product
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def seed_db(db: AsyncSession):
    """
    Seed the database with initial data.
    """
    # Seed Users
    users_to_create = [
        {"email": "user1@example.com", "hashed_password": get_password_hash("string")},
        {"email": "user2@example.com", "hashed_password": get_password_hash("string")},
    ]
    for user_data in users_to_create:
        result = await db.execute(select(User).where(User.email == user_data["email"]))
        if not result.scalar_one_or_none():
            db.add(User(**user_data))
            logger.info(f"Seeding user: {user_data['email']}")

    # Seed Products
    products_to_create = [
        {"name": "Laptop Pro", "description": "A powerful laptop", "price": 1200.00, "stock": 50},
        {"name": "Smartphone X", "description": "Latest generation smartphone", "price": 800.50, "stock": 150},
        {"name": "Wireless Headphones", "description": "Noise-cancelling headphones", "price": 250.75, "stock": 200},
        {"name": "Smart Watch 2", "description": "Fitness and notification watch", "price": 300.00, "stock": 80},
    ]
    for product_data in products_to_create:
        result = await db.execute(select(Product).where(Product.name == product_data["name"]))
        if not result.scalar_one_or_none():
            db.add(Product(**product_data))
            logger.info(f"Seeding product: {product_data['name']}")
    
    try:
        await db.commit()
    except IntegrityError:
        await db.rollback()
        logger.info("Data already exists, skipping seeding.")
    except Exception as e:
        await db.rollback()
        logger.error(f"Error seeding database: {e}")

async def main():
    logger.info("Creating initial data")
    async with AsyncSessionFactory() as session:
        await seed_db(session)
    logger.info("Initial data created")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
```

### `db/migrations/env.py`
```python
# db/migrations/env.py
import os
import sys
from logging.config import fileConfig

from alembic import context
from sqlalchemy import engine_from_config
from sqlalchemy.pool import NullPool
from sqlalchemy.ext.asyncio import AsyncEngine

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Add the project's root directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

# Import the Base from your models so that Alembic can see them
from db.base_class import Base
from db.models import user, product, cart # noqa

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Set the database URL from environment variable
config.set_main_option('sqlalchemy.url', os.environ['DATABASE_URL'])

target_metadata = Base.metadata

def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.
    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.
    Calls to context.execute() here emit the given string to the
    script output.
    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection):
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online() -> None:
    """Run migrations in 'online' mode.
    In this scenario we need to create an Engine
    and associate a connection with the context.
    """
    connectable = AsyncEngine(
        engine_from_config(
            config.get_section(config.config_ini_section),
            prefix="sqlalchemy.",
            poolclass=NullPool,
            future=True,
        )
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


if context.is_offline_mode():
    run_migrations_offline()
else:
    import asyncio
    asyncio.run(run_migrations_online())
```

### `db/migrations/versions/2024_05_21_1000_initial_schema.py`
```python
# db/migrations/versions/2024_05_21_1000_initial_schema.py
"""Initial schema

Revision ID: 1a2b3c4d5e6f
Revises: 
Create Date: 2024-05-21 10:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1a2b3c4d5e6f'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('products',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('description', sa.String(length=255), nullable=True),
    sa.Column('price', sa.Numeric(precision=10, scale=2), nullable=False),
    sa.Column('stock', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_products_id'), 'products', ['id'], unique=False)
    op.create_index(op.f('ix_products_name'), 'products', ['name'], unique=True)
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(length=255), nullable=False),
    sa.Column('hashed_password', sa.String(length=255), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    op.create_index(op.f('ix_users_id'), 'users', ['id'], unique=False)
    op.create_table('carts',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('user_id')
    )
    op.create_index(op.f('ix_carts_id'), 'carts', ['id'], unique=False)
    op.create_table('cartitems',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('cart_id', sa.Integer(), nullable=False),
    sa.Column('product_id', sa.Integer(), nullable=False),
    sa.Column('quantity', sa.Integer(), nullable=False),
    sa.CheckConstraint('quantity > 0', name='check_quantity_positive'),
    sa.ForeignKeyConstraint(['cart_id'], ['carts.id'], ),
    sa.ForeignKeyConstraint(['product_id'], ['products.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('cart_id', 'product_id', name='_cart_product_uc')
    )
    op.create_index(op.f('ix_cartitems_id'), 'cartitems', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_cartitems_id'), table_name='cartitems')
    op.drop_table('cartitems')
    op.drop_index(op.f('ix_carts_id'), table_name='carts')
    op.drop_table('carts')
    op.drop_index(op.f('ix_users_id'), table_name='users')
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_table('users')
    op.drop_index(op.f('ix_products_name'), table_name='products')
    op.drop_index(op.f('ix_products_id'), table_name='products')
    op.drop_table('products')
    # ### end Alembic commands ###
```

### `db/models/user.py`
```python
# db/models/user.py
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from db.base_class import Base

class User(Base):
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean(), default=True)
    
    cart = relationship("Cart", back_populates="user", uselist=False, cascade="all, delete-orphan")
```

### `db/models/product.py`
```python
# db/models/product.py
from sqlalchemy import Column, Integer, String, Numeric
from db.base_class import Base

class Product(Base):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, index=True, nullable=False)
    description = Column(String(255))
    price = Column(Numeric(10, 2), nullable=False)
    stock = Column(Integer, nullable=False)
```

### `db/models/cart.py`
```python
# db/models/cart.py
from sqlalchemy import (Column, Integer, ForeignKey, DateTime, func, UniqueConstraint, CheckConstraint)
from sqlalchemy.orm import relationship
from db.base_class import Base

class Cart(Base):
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    user = relationship("User", back_populates="cart")
    items = relationship("CartItem", back_populates="cart", cascade="all, delete-orphan")

class CartItem(Base):
    __tablename__ = 'cartitems'
    id = Column(Integer, primary_key=True, index=True)
    cart_id = Column(Integer, ForeignKey("carts.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    quantity = Column(Integer, nullable=False)

    cart = relationship("Cart", back_populates="items")
    product = relationship("Product")

    __table_args__ = (
        UniqueConstraint('cart_id', 'product_id', name='_cart_product_uc'),
        CheckConstraint('quantity > 0', name='check_quantity_positive'),
    )
```

### `schemas/cart.py`
```python
# schemas/cart.py
from pydantic import BaseModel, Field
from typing import List, Optional
from decimal import Decimal

# --- Request Schemas ---

class CartItemCreate(BaseModel):
    product_id: int = Field(..., gt=0, description="The ID of the product to add to the cart")
    quantity: int = Field(..., gt=0, description="The quantity of the product")

class CartItemUpdate(BaseModel):
    quantity: int = Field(..., gt=0, description="The new quantity for the cart item")

# --- Response Schemas ---

class ProductInCart(BaseModel):
    id: int
    name: str
    price: Decimal

    class Config:
        from_attributes = True

class CartItemView(BaseModel):
    id: int
    quantity: int
    product: ProductInCart
    item_total: Decimal

    class Config:
        from_attributes = True

class CartView(BaseModel):
    id: int
    user_id: int
    items: List[CartItemView]
    grand_total: Decimal
    total_items: int

    class Config:
        from_attributes = True
```

### `schemas/product.py`
```python
# schemas/product.py
from pydantic import BaseModel
from decimal import Decimal

class ProductBase(BaseModel):
    name: str
    description: str | None = None
    price: Decimal
    stock: int

class Product(ProductBase):
    id: int

    class Config:
        from_attributes = True
```

### `schemas/user.py`
```python
# schemas/user.py
from pydantic import BaseModel, EmailStr

class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    is_active: bool

    class Config:
        from_attributes = True
```

### `schemas/token.py`
```python
# schemas/token.py
from pydantic import BaseModel

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    user_id: int | None = None
```

### `schemas/msg.py`
```python
# schemas/msg.py
from pydantic import BaseModel

class Msg(BaseModel):
    msg: str
```

### `crud/base.py`
```python
# crud/base.py
# This file is intentionally left empty for this task.
# In a larger project, it would contain a generic CRUD base class.
```

### `crud/crud_cart.py`
```python
# crud/crud_cart.py
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from db.models.cart import Cart, CartItem
from db.models.product import Product

class CRUDCart:
    async def get_cart_by_user_id(self, db: AsyncSession, *, user_id: int) -> Cart | None:
        """
        Retrieve a user's cart, including all items and their associated product details.
        """
        stmt = (
            select(Cart)
            .where(Cart.user_id == user_id)
            .options(selectinload(Cart.items).selectinload(CartItem.product))
        )
        result = await db.execute(stmt)
        return result.scalar_one_or_none()

    async def create_cart(self, db: AsyncSession, *, user_id: int) -> Cart:
        """
        Create a new cart for a user.
        """
        db_cart = Cart(user_id=user_id)
        db.add(db_cart)
        await db.commit()
        await db.refresh(db_cart)
        return db_cart

    async def get_or_create_cart(self, db: AsyncSession, *, user_id: int) -> Cart:
        """
        Get a user's cart, or create one if it doesn't exist.
        """
        cart = await self.get_cart_by_user_id(db=db, user_id=user_id)
        if not cart:
            cart = await self.create_cart(db=db, user_id=user_id)
            # Re-fetch with relationships after creation
            cart = await self.get_cart_by_user_id(db=db, user_id=user_id)
        return cart

    async def add_item_to_cart(self, db: AsyncSession, *, cart: Cart, product_id: int, quantity: int) -> CartItem:
        """
        Add a product to the cart or update its quantity if it already exists.
        """
        # Check if item already exists in cart
        existing_item = next((item for item in cart.items if item.product_id == product_id), None)

        if existing_item:
            existing_item.quantity += quantity
            db_item = existing_item
        else:
            db_item = CartItem(cart_id=cart.id, product_id=product_id, quantity=quantity)
            db.add(db_item)
        
        await db.commit()
        await db.refresh(db_item)
        return db_item

    async def get_cart_item_by_id(self, db: AsyncSession, *, cart_item_id: int) -> CartItem | None:
        """
        Get a specific cart item by its ID.
        """
        stmt = select(CartItem).where(CartItem.id == cart_item_id)
        result = await db.execute(stmt)
        return result.scalar_one_or_none()

    async def update_cart_item_quantity(self, db: AsyncSession, *, db_item: CartItem, quantity: int) -> CartItem:
        """
        Update the quantity of a specific cart item.
        """
        db_item.quantity = quantity
        await db.commit()
        await db.refresh(db_item)
        return db_item

    async def remove_cart_item(self, db: AsyncSession, *, db_item: CartItem):
        """
        Remove an item from the cart.
        """
        await db.delete(db_item)
        await db.commit()

    async def get_product_by_id(self, db: AsyncSession, *, product_id: int) -> Product | None:
        """
        Get a product by its ID. Simulates fetching from a product service.
        """
        stmt = select(Product).where(Product.id == product_id)
        result = await db.execute(stmt)
        return result.scalar_one_or_none()

crud_cart = CRUDCart()
```

### `services/cart_service.py`
```python
# services/cart_service.py
from decimal import Decimal
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from crud.crud_cart import crud_cart
from schemas.cart import CartView, CartItemView, ProductInCart
from services.cache_service import CacheService

class CartService:
    def _get_cache_key(self, user_id: int) -> str:
        return f"cart:{user_id}"

    async def get_user_cart(self, db: AsyncSession, *, user_id: int) -> CartView | None:
        """
        Get the user's cart, from cache if available, otherwise from DB.
        """
        cache_key = self._get_cache_key(user_id)
        cached_cart = await CacheService.get(cache_key)
        if cached_cart:
            return CartView.model_validate(cached_cart)

        cart = await crud_cart.get_or_create_cart(db=db, user_id=user_id)
        if not cart:
            return None

        cart_view = self._create_cart_view(cart)
        await CacheService.set(cache_key, cart_view.model_dump(mode='json'))
        return cart_view

    def _create_cart_view(self, cart) -> CartView:
        """
        Helper to transform a Cart model into a CartView schema.
        """
        grand_total = Decimal("0.0")
        total_items = 0
        cart_item_views = []

        for item in cart.items:
            item_total = item.product.price * item.quantity
            grand_total += item_total
            total_items += item.quantity
            cart_item_views.append(
                CartItemView(
                    id=item.id,
                    quantity=item.quantity,
                    product=ProductInCart.model_validate(item.product),
                    item_total=item_total,
                )
            )
        
        return CartView(
            id=cart.id,
            user_id=cart.user_id,
            items=cart_item_views,
            grand_total=grand_total,
            total_items=total_items,
        )

    async def add_item(self, db: AsyncSession, *, user_id: int, product_id: int, quantity: int) -> CartView:
        """
        Adds an item to the user's cart and invalidates the cache.
        """
        product = await crud_cart.get_product_by_id(db=db, product_id=product_id)
        if not product:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
        
        if product.stock < quantity:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Not enough stock available")

        cart = await crud_cart.get_or_create_cart(db=db, user_id=user_id)
        
        # Check combined quantity if item is already in cart
        existing_item = next((item for item in cart.items if item.product_id == product_id), None)
        if existing_item and (existing_item.quantity + quantity > product.stock):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Not enough stock for combined quantity")

        await crud_cart.add_item_to_cart(db=db, cart=cart, product_id=product_id, quantity=quantity)
        
        await CacheService.delete(self._get_cache_key(user_id))
        
        # Return the updated cart view
        return await self.get_user_cart(db=db, user_id=user_id)

    async def update_item(self, db: AsyncSession, *, user_id: int, cart_item_id: int, quantity: int) -> CartView:
        """
        Updates an item's quantity in the cart and invalidates the cache.
        """
        cart_item = await crud_cart.get_cart_item_by_id(db=db, cart_item_id=cart_item_id)
        if not cart_item:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cart item not found")

        cart = await crud_cart.get_cart_by_user_id(db=db, user_id=user_id)
        if not cart or cart_item.cart_id != cart.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to update this item")

        product = await crud_cart.get_product_by_id(db=db, product_id=cart_item.product_id)
        if product.stock < quantity:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Not enough stock available")

        await crud_cart.update_cart_item_quantity(db=db, db_item=cart_item, quantity=quantity)
        
        await CacheService.delete(self._get_cache_key(user_id))
        return await self.get_user_cart(db=db, user_id=user_id)

    async def remove_item(self, db: AsyncSession, *, user_id: int, cart_item_id: int):
        """
        Removes an item from the cart and invalidates the cache.
        """
        cart_item = await crud_cart.get_cart_item_by_id(db=db, cart_item_id=cart_item_id)
        if not cart_item:
            # Idempotent: if it's already gone, that's fine.
            return

        cart = await crud_cart.get_cart_by_user_id(db=db, user_id=user_id)
        if not cart or cart_item.cart_id != cart.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to remove this item")

        await crud_cart.remove_cart_item(db=db, db_item=cart_item)
        await CacheService.delete(self._get_cache_key(user_id))

cart_service = CartService()
```

### `services/cache_service.py`
```python
# services/cache_service.py
import json
import logging
from typing import Any, Optional
import aioredis
from aioredis import Redis
from core.config import settings

logger = logging.getLogger(__name__)

class CacheService:
    redis: Optional[Redis] = None

    @classmethod
    async def initialize(cls):
        """
        Initializes the Redis connection pool.
        """
        if cls.redis is None:
            try:
                cls.redis = aioredis.from_url(
                    f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}",
                    encoding="utf-8",
                    decode_responses=True
                )
                await cls.redis.ping()
                logger.info("Successfully connected to Redis.")
            except Exception as e:
                logger.error(f"Failed to connect to Redis: {e}")
                cls.redis = None

    @classmethod
    async def close(cls):
        """
        Closes the Redis connection pool.
        """
        if cls.redis:
            await cls.redis.close()
            logger.info("Redis connection closed.")

    @classmethod
    async def get(cls, key: str) -> Optional[Any]:
        """
        Get a value from the cache.
        """
        if not cls.redis:
            return None
        value = await cls.redis.get(key)
        return json.loads(value) if value else None

    @classmethod
    async def set(cls, key: str, value: Any, expire: int = 3600):
        """
        Set a value in the cache with an expiration time.
        """
        if not cls.redis:
            return
        await cls.redis.set(key, json.dumps(value), ex=expire)

    @classmethod
    async def delete(cls, key: str):
        """
        Delete a key from the cache.
        """
        if not cls.redis:
            return
        await cls.redis.delete(key)
```

### `api/v1/api.py`
```python
# api/v1/api.py
from fastapi import APIRouter
from api.v1.endpoints import cart, login

api_router = APIRouter()
api_router.include_router(login.router, prefix="/login", tags=["login"])
api_router.include_router(cart.router, prefix="/cart", tags=["cart"])
```

### `api/v1/endpoints/login.py`
```python
# api/v1/endpoints/login.py
from datetime import timedelta
from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from core import security
from core.config import settings
from core.db import get_db
from db.models.user import User
from schemas.token import Token

router = APIRouter()

@router.post("/access-token", response_model=Token)
async def login_for_access_token(
    db: AsyncSession = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()
) -> Any:
    """
    OAuth2 compatible token login, get an access token for future requests.
    """
    result = await db.execute(select(User).where(User.email == form_data.username))
    user = result.scalar_one_or_none()

    if not user or not security.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = security.create_access_token(
        user.id, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
```

### `api/v1/endpoints/cart.py`
```python
# api/v1/endpoints/cart.py
from fastapi import APIRouter, Depends, status, Response
from sqlalchemy.ext.asyncio import AsyncSession

from core.db import get_db
from core.security import get_current_user
from db.models.user import User
from schemas.cart import CartView, CartItemCreate, CartItemUpdate
from schemas.msg import Msg
from services.cart_service import cart_service

router = APIRouter()

@router.get(
    "/",
    response_model=CartView,
    summary="Get the current user's shopping cart",
    description="Retrieves the full details of the shopping cart for the authenticated user.",
)
async def read_cart(
    *,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Retrieve the current user's cart.
    The cart is fetched from a cache if available, otherwise from the database.
    """
    cart = await cart_service.get_user_cart(db=db, user_id=current_user.id)
    return cart

@router.post(
    "/items",
    response_model=CartView,
    status_code=status.HTTP_201_CREATED,
    summary="Add an item to the cart",
    description="Adds a product with a specified quantity to the user's cart. If the product is already in the cart, its quantity is increased.",
)
async def add_item_to_cart(
    *,
    db: AsyncSession = Depends(get_db),
    item_in: CartItemCreate,
    current_user: User = Depends(get_current_user),
):
    """
    Add an item to the cart.
    - Validates product existence and stock.
    - Creates or updates the cart item.
    - Invalidates the cart cache.
    """
    cart = await cart_service.add_item(
        db=db,
        user_id=current_user.id,
        product_id=item_in.product_id,
        quantity=item_in.quantity,
    )
    return cart

@router.put(
    "/items/{cart_item_id}",
    response_model=CartView,
    summary="Update an item's quantity in the cart",
    description="Updates the quantity of a specific item in the user's cart.",
)
async def update_cart_item(
    *,
    db: AsyncSession = Depends(get_db),
    cart_item_id: int,
    item_in: CartItemUpdate,
    current_user: User = Depends(get_current_user),
):
    """
    Update a cart item's quantity.
    - Validates ownership of the cart item.
    - Validates product stock for the new quantity.
    - Invalidates the cart cache.
    """
    cart = await cart_service.update_item(
        db=db,
        user_id=current_user.id,
        cart_item_id=cart_item_id,
        quantity=item_in.quantity,
    )
    return cart

@router.delete(
    "/items/{cart_item_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Remove an item from the cart",
    description="Removes a specific item from the user's cart.",
)
async def remove_item_from_cart(
    *,
    db: AsyncSession = Depends(get_db),
    cart_item_id: int,
    current_user: User = Depends(get_current_user),
):
    """
    Remove an item from the cart.
    - Validates ownership of the cart item.
    - Is idempotent: does not fail if the item is already removed.
    - Invalidates the cart cache.
    """
    await cart_service.remove_item(
        db=db, user_id=current_user.id, cart_item_id=cart_item_id
    )
    return Response(status_code=status.HTTP_204_NO_CONTENT)
```

### `tests/conftest.py`
```python
# tests/conftest.py
import asyncio
from typing import AsyncGenerator, Generator

import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from core.config import settings
from core.db import get_db
from db.base_class import Base
from db.init_db import seed_db
from main import app
from core.security import create_access_token
from db.models.user import User

# Use a separate test database
TEST_DATABASE_URL = "sqlite+aiosqlite:///./test.db"

engine = create_async_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=AsyncSession)

@pytest.fixture(scope="session")
def event_loop() -> Generator:
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope="session", autouse=True)
async def setup_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    async with TestingSessionLocal() as session:
        await seed_db(session)

    yield

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

async def override_get_db() -> AsyncGenerator[AsyncSession, None]:
    async with TestingSessionLocal() as session:
        yield session

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(scope="module")
def client() -> Generator:
    with TestClient(app) as c:
        yield c

@pytest.fixture(scope="module")
async def async_client() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac

@pytest.fixture(scope="module")
def user1_token_headers(client: TestClient) -> dict[str, str]:
    token = create_access_token(1)
    return {"Authorization": f"Bearer {token}"}

@pytest.fixture(scope="module")
def user2_token_headers(client: TestClient) -> dict[str, str]:
    token = create_access_token(2)
    return {"Authorization": f"Bearer {token}"}
```

### `tests/test_cart_api.py`
```python
# tests/test_cart_api.py
import pytest
from httpx import AsyncClient

API_V1_STR = "/api/v1"

@pytest.mark.asyncio
async def test_get_empty_cart(async_client: AsyncClient, user1_token_headers: dict):
    response = await async_client.get(f"{API_V1_STR}/cart/", headers=user1_token_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["user_id"] == 1
    assert data["items"] == []
    assert data["grand_total"] == 0
    assert data["total_items"] == 0

@pytest.mark.asyncio
async def test_add_item_to_cart(async_client: AsyncClient, user1_token_headers: dict):
    # Add a laptop
    response = await async_client.post(
        f"{API_V1_STR}/cart/items",
        json={"product_id": 1, "quantity": 1},
        headers=user1_token_headers,
    )
    assert response.status_code == 201
    data = response.json()
    assert data["total_items"] == 1
    assert len(data["items"]) == 1
    assert data["items"][0]["product"]["name"] == "Laptop Pro"
    assert data["items"][0]["quantity"] == 1
    assert data["grand_total"] == "1200.00"

@pytest.mark.asyncio
async def test_add_existing_item_to_cart(async_client: AsyncClient, user1_token_headers: dict):
    # Add another laptop, quantity should increase
    response = await async_client.post(
        f"{API_V1_STR}/cart/items",
        json={"product_id": 1, "quantity": 1},
        headers=user1_token_headers,
    )
    assert response.status_code == 201
    data = response.json()
    assert data["total_items"] == 2
    assert len(data["items"]) == 1
    assert data["items"][0]["quantity"] == 2
    assert data["grand_total"] == "2400.00"

@pytest.mark.asyncio
async def test_add_different_item_to_cart(async_client: AsyncClient, user1_token_headers: dict):
    # Add a smartphone
    response = await async_client.post(
        f"{API_V1_STR}/cart/items",
        json={"product_id": 2, "quantity": 2},
        headers=user1_token_headers,
    )
    assert response.status_code == 201
    data = response.json()
    assert data["total_items"] == 4 # 2 laptops + 2 smartphones
    assert len(data["items"]) == 2
    assert data["grand_total"] == "4001.00" # 2400 + 1601

@pytest.mark.asyncio
async def test_update_cart_item_quantity(async_client: AsyncClient, user1_token_headers: dict):
    # Get cart to find item id
    get_response = await async_client.get(f"{API_V1_STR}/cart/", headers=user1_token_headers)
    cart_data = get_response.json()
    laptop_item = next(item for item in cart_data["items"] if item["product"]["id"] == 1)
    
    # Update laptop quantity to 3
    response = await async_client.put(
        f"{API_V1_STR}/cart/items/{laptop_item['id']}",
        json={"quantity": 3},
        headers=user1_token_headers,
    )
    assert response.status_code == 200
    data = response.json()
    assert data["total_items"] == 5 # 3 laptops + 2 smartphones
    updated_laptop_item = next(item for item in data["items"] if item["product"]["id"] == 1)
    assert updated_laptop_item["quantity"] == 3
    assert data["grand_total"] == "5201.00" # 3600 + 1601

@pytest.mark.asyncio
async def test_remove_cart_item(async_client: AsyncClient, user1_token_headers: dict):
    # Get cart to find item id
    get_response = await async_client.get(f"{API_V1_STR}/cart/", headers=user1_token_headers)
    cart_data = get_response.json()
    smartphone_item = next(item for item in cart_data["items"] if item["product"]["id"] == 2)

    # Remove smartphone
    response = await async_client.delete(
        f"{API_V1_STR}/cart/items/{smartphone_item['id']}",
        headers=user1_token_headers,
    )
    assert response.status_code == 204

    # Verify cart state
    get_response_after_delete = await async_client.get(f"{API_V1_STR}/cart/", headers=user1_token_headers)
    data = get_response_after_delete.json()
    assert data["total_items"] == 3
    assert len(data["items"]) == 1
    assert data["items"][0]["product"]["id"] == 1 # Only laptop remains
    assert data["grand_total"] == "3600.00"

@pytest.mark.asyncio
async def test_add_item_insufficient_stock(async_client: AsyncClient, user1_token_headers: dict):
    # Product 1 (Laptop Pro) has 50 stock
    response = await async_client.post(
        f"{API_V1_STR}/cart/items",
        json={"product_id": 1, "quantity": 100},
        headers=user1_token_headers,
    )
    assert response.status_code == 400
    assert "Not enough stock" in response.json()["detail"]

@pytest.mark.asyncio
async def test_user_cannot_access_another_users_cart_item(async_client: AsyncClient, user1_token_headers: dict, user2_token_headers: dict):
    # User 2 adds an item
    await async_client.post(
        f"{API_V1_STR}/cart/items",
        json={"product_id": 3, "quantity": 1},
        headers=user2_token_headers,
    )
    
    # Get user 2's cart to find item id
    get_response = await async_client.get(f"{API_V1_STR}/cart/", headers=user2_token_headers)
    cart_data = get_response.json()
    user2_item_id = cart_data["items"][0]["id"]
    
    # User 1 tries to update user 2's item
    response = await async_client.put(
        f"{API_V1_STR}/cart/items/{user2_item_id}",
        json={"quantity": 5},
        headers=user1_token_headers,
    )
    assert response.status_code == 403
    assert "Not authorized" in response.json()["detail"]
    
    # User 1 tries to delete user 2's item
    response = await async_client.delete(
        f"{API_V1_STR}/cart/items/{user2_item_id}",
        headers=user1_token_headers,
    )
    assert response.status_code == 403
    assert "Not authorized" in response.json()["detail"]
```
✅ Streaming completed.