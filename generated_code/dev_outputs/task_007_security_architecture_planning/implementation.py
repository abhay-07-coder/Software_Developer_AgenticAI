## Security Architecture Plan

This document outlines the comprehensive security strategy for the microservices-based application. It covers authentication, authorization, data protection, and proactive vulnerability mitigation, establishing a security-first posture for the entire system. This plan is designed to be a living document, evolving as the system and threat landscape change.

### 1. Introduction

Security is a foundational pillar of our application architecture. In a distributed microservices environment, a robust and clearly defined security model is critical to protect user data, maintain system integrity, and build trust. This plan addresses security at multiple layers, from the network to the application code, ensuring a defense-in-depth approach.

The primary goals of this security architecture are:
- **Confidentiality:** Protecting data from unauthorized disclosure.
- **Integrity:** Ensuring data is accurate and has not been tampered with.
- **Availability:** Guaranteeing that services are accessible to legitimate users.
- **Accountability:** Tracing actions back to specific users or services.

This plan is built upon the microservices architecture defined in `task_003`, with a dedicated **Auth Service** acting as the central authority for authentication and token issuance.

### 2. Threat Model (STRIDE)

We use the STRIDE model to categorize and proactively address potential threats.

-   **Spoofing:** An attacker impersonates a legitimate user or service.
    -   **Mitigation:** Strong authentication using JWTs. Service-to-service communication will also be authenticated, potentially using mTLS or service-specific JWTs.
-   **Tampering:** Unauthorized modification of data in transit or at rest.
    -   **Mitigation:** TLS for all network traffic. Digital signatures in JWTs to prevent token tampering. Database-level integrity checks and transaction logs.
-   **Repudiation:** A user denies performing an action.
    -   **Mitigation:** Comprehensive audit trails. All sensitive operations (e.g., login, data modification, password change) will be logged with user ID, timestamp, and IP address.
-   **Information Disclosure:** Exposure of sensitive data to unauthorized parties.
    -   **Mitigation:** RBAC to enforce the principle of least privilege. Encryption of data at rest and in transit. Strict input/output validation to prevent data leakage through error messages or APIs.
-   **Denial of Service (DoS):** Overwhelming a service to make it unavailable.
    -   **Mitigation:** Rate limiting on the API Gateway and individual services. Use of scalable cloud infrastructure with auto-scaling and load balancing. Protection against resource exhaustion via strict input validation (e.g., limiting payload size).
-   **Elevation of Privilege:** A user gains access to capabilities beyond their authorized level.
    -   **Mitigation:** Strict RBAC enforcement on every API request. Short-lived access tokens. Secure validation of all authorization claims within tokens.

### 3. Authentication Strategy

Authentication is the process of verifying a user's identity. We will adopt a centralized, token-based authentication model using JSON Web Tokens (JWT).

#### 3.1. Mechanism: JWT (JSON Web Tokens)

JWTs are chosen for their suitability in stateless, distributed systems:
-   **Stateless:** The user's session is stored on the client, reducing server load and simplifying horizontal scaling.
-   **Self-Contained:** The token contains all necessary user information (ID, roles, etc.) for services to make authorization decisions without querying the Auth Service on every request.
-   **Secure:** Tokens are digitally signed (using HMAC with SHA-256, i.e., HS256) to prevent tampering.

#### 3.2. Token Flow & Structure

We will use a two-token system:
1.  **Access Token:**
    -   **Purpose:** Grants access to protected resources. Included in the `Authorization` header of every API request.
    -   **Payload:** Contains user ID, roles, and an expiration claim (`exp`).
    -   **Lifespan:** Short-lived (e.g., **15 minutes**) to limit the impact of a compromised token.
2.  **Refresh Token:**
    -   **Purpose:** Used to obtain a new access token without requiring the user to re-enter credentials.
    -   **Storage:** Stored securely on the client (e.g., an `HttpOnly`, `Secure`, `SameSite=Strict` cookie) to mitigate XSS attacks.
    -   **Lifespan:** Long-lived (e.g., **7 days**).
    -   **Security:** Refresh tokens are stored in the database and can be individually revoked if compromised.

#### 3.3. Password Management

-   **Hashing Algorithm:** **Argon2id** is the chosen algorithm.
    -   **Justification:** Argon2 was the winner of the Password Hashing Competition (PHC). It is highly resistant to both GPU cracking attacks (memory-hardness) and side-channel attacks. It is superior to bcrypt, which is not memory-hard, and scrypt, which is vulnerable to certain side-channel attacks. We will use the `passlib` library for a robust implementation.
-   **Password Policy:**
    -   Minimum length: 12 characters.
    -   Complexity: Must contain at least one uppercase letter, one lowercase letter, one number, and one special character.
    -   Breached Password Check: Passwords will be checked against a known data breach service (like Have I Been Pwned) upon registration or update.

### 4. Authorization Strategy

Authorization determines what an authenticated user is allowed to do. We will implement a Role-Based Access Control (RBAC) model.

#### 4.1. Model: Role-Based Access Control (RBAC)

-   **Users:** Individual entities that can log in.
-   **Roles:** Collections of permissions. A user is assigned one or more roles.
-   **Permissions:** Specific actions that can be performed on a resource (e.g., `create:product`, `read:order`, `delete:user`).

#### 4.2. Role Definitions (Initial Set)

-   `User`: The default role for all registered customers.
    -   Permissions: Read products, create/read their own orders, manage their own user profile.
-   `Admin`: A superuser with full system access.
    -   Permissions: All permissions, including managing users, roles, and all data across services.
-   `Service`: A role for internal, service-to-service communication.
    -   Permissions: Specific permissions required for inter-service calls (e.g., Order Service can request product details from Product Service).

#### 4.3. Enforcement

-   The user's roles will be embedded in the `roles` claim of the JWT access token.
-   An API Gateway (or middleware in each microservice) will inspect the access token on every incoming request.
-   It will validate the token's signature and expiration.
-   It will check if the roles listed in the token grant the necessary permission for the requested endpoint and method.
-   Requests with invalid tokens or insufficient permissions will be rejected with a `401 Unauthorized` or `403 Forbidden` status.

### 5. Data Encryption

-   **Encryption in Transit:** All communication channels MUST use **TLS 1.2 or higher**. This includes:
    -   Client to API Gateway.
    -   API Gateway to microservices.
    -   Inter-service communication.
    -   Service to database/cache.
-   **Encryption at Rest:** All sensitive data stored in databases (PostgreSQL) or object storage (S3) MUST be encrypted. This can be achieved using the native encryption features of the cloud provider (e.g., AWS RDS Encryption, S3 Server-Side Encryption).

### 6. Vulnerability Mitigation

-   **Input Validation:** All incoming data (request bodies, query parameters, headers) will be strictly validated using Pydantic schemas in FastAPI. This prevents a wide range of attacks, including injection and buffer overflows.
-   **SQL Injection:** We will exclusively use an ORM (SQLAlchemy) with parameterized queries. Raw SQL queries are forbidden.
-   **Cross-Site Scripting (XSS):**
    -   **Backend:** Set a strict **Content-Security-Policy (CSP)** header. Ensure API responses have the correct `Content-Type` (e.g., `application/json`) to prevent browsers from misinterpreting them as HTML.
    -   **Frontend:** Frameworks like React automatically escape data rendered in JSX, providing a strong defense. Developers must avoid dangerous practices like using `dangerouslySetInnerHTML`.
-   **Cross-Site Request Forgery (CSRF):** Since we use JWTs in the `Authorization` header, we are not vulnerable to traditional CSRF attacks that rely on cookies being sent automatically by the browser. If refresh tokens are stored in cookies, they must use the `SameSite=Strict` attribute.
-   **Rate Limiting:** Implement IP-based and user-ID-based rate limiting at the API Gateway level using a Redis-backed store. This protects against brute-force login attempts and DoS attacks.
-   **Security Headers:** All API responses will include the following headers:
    -   `Strict-Transport-Security`: Enforces HTTPS.
    -   `X-Content-Type-Options: nosniff`: Prevents MIME-type sniffing.
    -   `X-Frame-Options: DENY`: Prevents clickjacking.
    -   `Content-Security-Policy`: Restricts sources for content.

### 7. Secrets Management

-   **Local Development:** Use `.env` files (which are git-ignored) for secrets.
-   **Staging/Production:** All secrets (database credentials, API keys, JWT secret key) MUST be stored in a dedicated secrets management service like **AWS Secrets Manager** or **HashiCorp Vault**. Applications will fetch secrets at runtime using IAM roles, not from environment variables or configuration files.

### 8. Logging and Monitoring

-   **Audit Trails:** Log all security-relevant events (e.g., successful/failed logins, password changes, role modifications, resource deletion) to a centralized logging system (e.g., ELK Stack, Datadog).
-   **Security Monitoring & Alerting:** Configure automated alerts for suspicious patterns:
    -   High rate of failed login attempts from a single IP or for a single user.
    -   Authorization failures indicating potential privilege escalation attempts.
    -   Unexpected errors or exceptions.
-   **Health Checks:** Each service will expose a `/health` endpoint for monitoring by orchestration tools like Kubernetes.

### 9. CI/CD Security (DevSecOps)

Security will be integrated directly into our CI/CD pipeline.
-   **Static Application Security Testing (SAST):** Run tools like `bandit` on every commit to find common security issues in Python code.
-   **Software Composition Analysis (SCA):** Use `pip-audit` or integrated tools like Snyk/Dependabot to scan for vulnerabilities in third-party dependencies.
-   **Container Scanning:** Scan Docker images for known OS-level vulnerabilities before pushing to the registry.
-   **Secret Scanning:** Integrate tools to prevent secrets from being accidentally committed to the repository.

---

## Auth Service - Foundational Implementation

The following code artifacts provide a production-ready foundation for the **Auth Service** as described in the security plan.

### `.env.example`
This file shows the required environment variables for configuration. Create a `.env` file based on this example for local development.

```ini
# .env.example
# Application Configuration
DATABASE_URL="postgresql://user:password@localhost/auth_db"
SECRET_KEY="a_very_secret_key_that_is_long_and_random" # Should be a 64-character hex string in production
ALGORITHM="HS256"

# Token Lifespan (in minutes)
ACCESS_TOKEN_EXPIRE_MINUTES=15
REFRESH_TOKEN_EXPIRE_MINUTES=10080 # 7 days
```

### `requirements.txt`
List of all Python dependencies for the Auth Service.

```text
# requirements.txt
fastapi[all]
uvicorn[standard]
sqlalchemy
psycopg2-binary
alembic
python-dotenv
passlib[argon2]
python-jose[cryptography]
pydantic[email]
```

### `config.py`
Configuration management using Pydantic's `BaseSettings` to load from environment variables.

```python
# auth_service/config.py
import os
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.
    """
    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days

    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'

settings = Settings()
```

### `database.py`
SQLAlchemy setup for database connection and session management.

```python
# auth_service/database.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings

engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    """
    FastAPI dependency to get a database session.
    Ensures the session is closed after the request.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

### `models.py`
SQLAlchemy ORM models for Users and Roles, defining the database schema for RBAC.

```python
# auth_service/models.py
import uuid
from sqlalchemy import Column, String, Boolean, ForeignKey, Table
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from .database import Base

# Association table for the many-to-many relationship between users and roles
user_roles = Table('user_roles', Base.metadata,
    Column('user_id', UUID(as_uuid=True), ForeignKey('users.id'), primary_key=True),
    Column('role_id', UUID(as_uuid=True), ForeignKey('roles.id'), primary_key=True)
)

class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)

    roles = relationship("Role", secondary=user_roles, back_populates="users")

class Role(Base):
    __tablename__ = "roles"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, unique=True, index=True, nullable=False)
    description = Column(String)

    users = relationship("User", secondary=user_roles, back_populates="roles")
```

### `schemas.py`
Pydantic schemas for data validation and serialization.

```python
# auth_service/schemas.py
from pydantic import BaseModel, EmailStr, Field
import uuid

# --- Token Schemas ---
class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    email: EmailStr | None = None
    roles: list[str] = []

# --- User & Role Schemas ---
class RoleBase(BaseModel):
    name: str
    description: str | None = None

class RoleCreate(RoleBase):
    pass

class Role(RoleBase):
    id: uuid.UUID

    class Config:
        from_attributes = True

class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    password: str = Field(..., min_length=12)

class User(UserBase):
    id: uuid.UUID
    is_active: bool
    roles: list[Role] = []

    class Config:
        from_attributes = True
```

### `security.py`
Core security utilities for password hashing and JWT management.

```python
# auth_service/security.py
from datetime import datetime, timedelta, timezone
from passlib.context import CryptContext
from jose import JWTError, jwt
from .config import settings
from . import schemas

# Use Argon2 for password hashing
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifies a plain password against a hashed one."""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """Hashes a plain password."""
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    """Creates a new JWT access token."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def create_refresh_token(data: dict) -> str:
    """Creates a new JWT refresh token."""
    expires = timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES)
    return create_access_token(data, expires_delta=expires)

def decode_token(token: str) -> schemas.TokenData | None:
    """Decodes a JWT, returning the payload if valid."""
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email: str = payload.get("sub")
        roles: list = payload.get("roles", [])
        if email is None:
            return None
        return schemas.TokenData(email=email, roles=roles)
    except JWTError:
        return None
```

### `dependencies.py`
FastAPI dependencies for enforcing authentication and authorization.

```python
# auth_service/dependencies.py
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from . import security, crud, schemas, models
from .database import get_db

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

def get_current_user(
    token: str = Depends(oauth2_scheme), 
    db: Session = Depends(get_db)
) -> models.User:
    """
    Dependency to get the current user from a JWT token.
    Raises HTTPException if the token is invalid or the user doesn't exist.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    token_data = security.decode_token(token)
    if token_data is None or token_data.email is None:
        raise credentials_exception
    
    user = crud.get_user_by_email(db, email=token_data.email)
    if user is None or not user.is_active:
        raise credentials_exception
    return user

class RoleChecker:
    """
    Dependency that checks if the current user has the required roles.
    """
    def __init__(self, allowed_roles: list[str]):
        self.allowed_roles = allowed_roles

    def __call__(self, current_user: models.User = Depends(get_current_user)):
        user_roles = {role.name for role in current_user.roles}
        if not any(role in user_roles for role in self.allowed_roles):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Operation not permitted: Insufficient roles",
            )
```

### `crud.py`
Database operations (Create, Read, Update, Delete) for users and roles.

```python
# auth_service/crud.py
from sqlalchemy.orm import Session
from . import models, schemas, security

def get_user_by_email(db: Session, email: str) -> models.User | None:
    """Fetches a user by their email address."""
    return db.query(models.User).filter(models.User.email == email).first()

def create_user(db: Session, user: schemas.UserCreate) -> models.User:
    """Creates a new user in the database with a hashed password."""
    hashed_password = security.get_password_hash(user.password)
    db_user = models.User(email=user.email, hashed_password=hashed_password)
    
    # Assign default 'User' role
    user_role = get_role_by_name(db, "User")
    if user_role:
        db_user.roles.append(user_role)

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_role_by_name(db: Session, name: str) -> models.Role | None:
    """Fetches a role by its name."""
    return db.query(models.Role).filter(models.Role.name == name).first()

def create_role(db: Session, role: schemas.RoleCreate) -> models.Role:
    """Creates a new role."""
    db_role = models.Role(**role.dict())
    db.add(db_role)
    db.commit()
    db.refresh(db_role)
    return db_role
```

### `main.py`
The main FastAPI application file with routes and security middleware.

```python
# auth_service/main.py
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta

from . import crud, schemas, security, models, dependencies
from .database import get_db, engine
from .config import settings

# Create database tables on startup if they don't exist
# In production, this should be handled by Alembic migrations
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Authentication Service",
    description="Handles user authentication, authorization, and token management.",
    version="1.0.0"
)

@app.post("/auth/token", response_model=schemas.Token)
def login_for_access_token(
    db: Session = Depends(get_db), 
    form_data: OAuth2PasswordRequestForm = Depends()
):
    """
    Authenticates a user and returns an access and refresh token.
    """
    user = crud.get_user_by_email(db, email=form_data.username)
    if not user or not security.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    user_roles = [role.name for role in user.roles]
    token_data = {"sub": user.email, "roles": user_roles}
    
    access_token = security.create_access_token(data=token_data)
    refresh_token = security.create_refresh_token(data={"sub": user.email}) # Refresh token has fewer claims
    
    return {
        "access_token": access_token, 
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }

@app.post("/users/", response_model=schemas.User, status_code=status.HTTP_201_CREATED)
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """
    Registers a new user.
    """
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)

@app.get("/users/me", response_model=schemas.User)
def read_users_me(current_user: models.User = Depends(dependencies.get_current_user)):
    """
    Returns the profile of the currently authenticated user.
    """
    return current_user

@app.get("/admin/dashboard", dependencies=[Depends(dependencies.RoleChecker(["Admin"]))])
def get_admin_dashboard():
    """
    An example of an admin-only protected endpoint.
    """
    return {"message": "Welcome to the Admin Dashboard!"}

@app.on_event("startup")
def startup_event():
    """
    Seed the database with initial roles on application startup.
    This is for demonstration; in production, use a dedicated seeding script.
    """
    db = next(get_db())
    try:
        if not crud.get_role_by_name(db, "User"):
            crud.create_role(db, schemas.RoleCreate(name="User", description="Standard user"))
        if not crud.get_role_by_name(db, "Admin"):
            crud.create_role(db, schemas.RoleCreate(name="Admin", description="System administrator"))
    finally:
        db.close()

@app.get("/health")
def health_check():
    """
    Health check endpoint for monitoring.
    """
    return {"status": "ok"}
```

### `Dockerfile`
A multi-stage Dockerfile for building a lean, production-ready container image.

```dockerfile
# Dockerfile

# --- Build Stage ---
FROM python:3.11-slim as builder

WORKDIR /usr/src/app

# Set environment variables to prevent writing .pyc files and to buffer output
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install build dependencies
RUN pip install --upgrade pip
COPY requirements.txt .
RUN pip wheel --no-cache-dir --wheel-dir /usr/src/app/wheels -r requirements.txt

# --- Final Stage ---
FROM python:3.11-slim

WORKDIR /usr/src/app

# Create a non-root user for security
RUN addgroup --system app && adduser --system --group app

# Copy built wheels from the builder stage
COPY --from=builder /usr/src/app/wheels /wheels

# Install dependencies from wheels
RUN pip install --no-cache /wheels/*

# Copy application code
COPY . .

# Change ownership to the non-root user
RUN chown -R app:app /usr/src/app

# Switch to the non-root user
USER app

# Expose the port the app runs on
EXPOSE 8000

# Run the application
CMD ["uvicorn", "auth_service.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Setup and Deployment Instructions

1.  **Dependencies:** Install Python 3.11+, Docker, and a PostgreSQL database.
2.  **Environment:** Create a `.env` file in the project root from the `.env.example` template and fill in your database URL and a securely generated `SECRET_KEY`.
3.  **Install Packages:** `pip install -r requirements.txt`
4.  **Database Migrations:** While the example uses `create_all`, a production setup should use Alembic.
    -   `alembic init alembic` (one-time setup)
    -   Modify `alembic.ini` and `alembic/env.py` to point to your database.
    -   `alembic revision --autogenerate -m "Initial migration"`
    -   `alembic upgrade head`
5.  **Run Locally:** `uvicorn auth_service.main:app --reload`
6.  **Build Docker Image:** `docker build -t auth-service:latest .`
7.  **Run with Docker:** `docker run -d -p 8000:8000 --env-file .env --name auth-service auth-service:latest`
✅ Streaming completed.