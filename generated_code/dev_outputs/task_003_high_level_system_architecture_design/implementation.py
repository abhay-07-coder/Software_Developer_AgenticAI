## High-Level System Architecture

This document outlines the high-level system architecture for the e-commerce platform. The design prioritizes scalability, maintainability, and resilience by adopting a microservices pattern.

### 1. Architectural Approach: Microservices

A **Microservices Architecture** has been chosen over a traditional monolith. This approach decomposes the application into a collection of loosely coupled, independently deployable services.

**Rationale:**
*   **Scalability:** Each service (e.g., Product Catalog, Order Management) can be scaled independently based on its specific load, optimizing resource usage.
*   **Technology Flexibility:** Each service can be built with the most appropriate technology stack, although we will standardize on Python/FastAPI for consistency initially.
*   **Resilience:** Failure in one service is isolated and, with proper design (e.g., circuit breakers), will not cause a catastrophic failure of the entire application.
*   **Maintainability:** Smaller, focused codebases are easier to understand, maintain, and test.
*   **Team Autonomy:** Enables smaller, autonomous teams to own the full lifecycle of their services, from development to deployment and operation.

### 2. Architecture Diagram

The following diagram illustrates the major components and the flow of data between them.

```mermaid
graph TD
    subgraph "Clients"
        WebApp[Web Application (React/Vue)]
        MobileApp[Mobile Application (iOS/Android)]
    end

    subgraph "Cloud Infrastructure (AWS/GCP/Azure)"
        API_Gateway[API Gateway]

        subgraph "Core Services"
            AuthService[Auth Service<br>(PostgreSQL)]
            UserService[User Service<br>(PostgreSQL)]
            ProductService[Product Service<br>(PostgreSQL, Elasticsearch)]
            OrderService[Order Service<br>(PostgreSQL)]
            CartService[Cart Service<br>(Redis)]
            NotificationService[Notification Service]
        end

        subgraph "Supporting Infrastructure"
            MessageBroker[(Message Broker<br>RabbitMQ / Kafka)]
            ServiceRegistry[Service Registry<br>(Consul / Kubernetes DNS)]
            Monitoring[Monitoring & Logging<br>(Prometheus, Grafana, ELK)]
        end

        subgraph "Third-Party Integrations"
            PaymentGateway[Payment Gateway<br>(Stripe / Braintree)]
        end
    end

    %% Connections
    WebApp --> API_Gateway
    MobileApp --> API_Gateway

    API_Gateway -->|/auth/**| AuthService
    API_Gateway -->|/users/**| UserService
    API_Gateway -->|/products/**| ProductService
    API_Gateway -->|/orders/**| OrderService
    API_Gateway -->|/cart/**| CartService

    OrderService -->|Processes Payment| PaymentGateway
    OrderService -- Publishes 'OrderCreated' --> MessageBroker
    ProductService -- Publishes 'ProductUpdated' --> MessageBroker

    MessageBroker -- Consumes 'OrderCreated' --> NotificationService
    MessageBroker -- Consumes 'OrderCreated' --> ProductService
    
    ProductService -->|Indexes Data| Elasticsearch

    %% Internal Service Communication (Example)
    OrderService -->|Gets Product Details| ProductService
```

### 3. Core Components & Responsibilities

| Service               | Responsibilities                                                                                             | Database         |
| --------------------- | ------------------------------------------------------------------------------------------------------------ | ---------------- |
| **API Gateway**       | Single entry point for all clients. Handles request routing, rate limiting, CORS, and initial authentication.  | N/A              |
| **Auth Service**      | Manages user registration, login (authentication), JWT generation and validation, and password management.     | PostgreSQL       |
| **User Service**      | Manages user profiles, shipping/billing addresses, and other non-auth related user data.                     | PostgreSQL       |
| **Product Service**   | Manages product catalog, categories, inventory, pricing, and detailed product information. Powers search via Elasticsearch. | PostgreSQL, Elasticsearch |
| **Order Service**     | Handles order creation, state management (e.g., PENDING, SHIPPED), payment processing, and order history.      | PostgreSQL       |
| **Cart Service**      | Manages user shopping carts. Supports both authenticated and anonymous users. High-performance.                | Redis            |
| **Notification Service**| Sends transactional emails, SMS, and push notifications (e.g., order confirmation, password reset).          | N/A              |

### 4. Communication Patterns

A hybrid communication model will be employed to leverage the strengths of different patterns.

#### 4.1. Synchronous Communication: REST APIs

*   **Pattern:** Direct service-to-service communication via RESTful APIs over HTTP.
*   **Use Cases:**
    *   Client-to-Backend: All initial requests from the web/mobile clients to the API Gateway.
    *   Internal Requests Requiring Immediate Response: The API Gateway validating a token with the Auth Service, or the Order Service fetching product price details from the Product Service during order creation.
*   **Pros:** Simple, well-understood, and suitable for request/response interactions.
*   **Cons:** Creates temporal coupling. If the called service is down, the caller is blocked or fails. This will be mitigated using patterns like Timeouts, Retries, and Circuit Breakers.

#### 4.2. Asynchronous Communication: Event-Driven

*   **Pattern:** Services communicate by publishing and consuming events via a central **Message Broker** (e.g., RabbitMQ).
*   **Use Cases:**
    *   **Decoupling Services:** When an order is created, the `Order Service` publishes an `OrderCreated` event. The `Product Service` subscribes to this to decrement stock, and the `Notification Service` subscribes to send a confirmation email. The `Order Service` does not need to know about these downstream consumers.
    *   **Improving Resilience:** If the `Notification Service` is temporarily down, the `OrderCreated` events will queue in the message broker and be processed once the service recovers.
*   **Pros:** Decouples services, improves fault tolerance, and enables complex workflows.
*   **Cons:** Adds complexity (requires managing a message broker) and makes end-to-end tracing more difficult (requires distributed tracing tools).

### 5. Data Management Strategy

The **Database-per-Service** pattern will be strictly followed.

*   **Principle:** Each microservice owns its domain data and is solely responsible for its database. No other service is allowed to access another service's database directly.
*   **Rationale:** This ensures loose coupling. Changes to one service's database schema do not impact other services. It also allows each service to choose the database technology best suited for its needs (e.g., PostgreSQL for transactional data, Redis for caching, Elasticsearch for search).
*   **Data Consistency:** Data consistency across services will be managed through eventual consistency, primarily using the event-driven pattern described above. For business processes requiring strong consistency, a Saga pattern can be implemented.

### 6. Technology Stack Summary

| Category                  | Technology / Tool                                | Rationale                                                              |
| ------------------------- | ------------------------------------------------ | ---------------------------------------------------------------------- |
| **Backend Framework**     | Python 3.11+ / FastAPI                          | High performance, modern, excellent typing support, auto-generated docs. |
| **Containerization**      | Docker                                           | Standard for packaging applications and their dependencies.            |
| **Orchestration**         | Kubernetes (K8s)                                 | Industry standard for deploying, scaling, and managing containers.     |
| **Relational Database**   | PostgreSQL 15+                                   | Powerful, reliable, and feature-rich open-source RDBMS.                |
| **In-Memory/Cache DB**    | Redis 7+                                         | High-performance key-value store for caching, sessions, and carts.     |
| **Search Engine**         | Elasticsearch                                    | Advanced full-text search, analytics, and filtering capabilities.      |
| **Message Broker**        | RabbitMQ                                         | Mature, reliable, and versatile message broker for async communication. |
| **API Gateway**           | Custom (FastAPI) or Kong/Tyk                     | Centralized request handling. A custom gateway offers max flexibility. |
| **CI/CD**                 | GitHub Actions                                   | Tightly integrated with source control for automated builds and deploys. |
| **Monitoring**            | Prometheus (Metrics), Grafana (Dashboards)       | Powerful open-source stack for monitoring and alerting.                |
| **Logging**               | ELK Stack (Elasticsearch, Logstash, Kibana)      | Centralized logging for debugging and analysis in a distributed system. |

### 7. Project Directory Structure

A monorepo structure is proposed to simplify dependency management and cross-service development in the initial stages.

```plaintext
/ecommerce-platform/
├── .github/
│   └── workflows/
│       ├── ci.yml          # Continuous Integration pipeline
│       └── cd.yml          # Continuous Deployment pipeline
├── docs/
│   └── architecture.md     # This document
├── infrastructure/
│   ├── docker-compose.yml  # For local development
│   └── kubernetes/
│       ├── api-gateway/
│       ├── auth-service/
│       └── ... (k8s manifests for each service)
└── services/
    ├── api-gateway/
    │   ├── app/
    │   ├── tests/
    │   ├── Dockerfile
    │   └── requirements.txt
    ├── auth-service/
    │   ├── app/
    │   ├── tests/
    │   ├── Dockerfile
    │   └── requirements.txt
    ├── product-service/
    │   └── ...
    ├── order-service/
    │   └── ...
    └── ... (other services)
```

### 8. Initial Implementation & Proof of Concept

To demonstrate the core architectural patterns, the following section provides a deployable proof-of-concept for the **API Gateway** and **Auth Service**, showcasing secure inter-service communication.

---

## Proof of Concept: API Gateway & Auth Service

This implementation provides a runnable example of two core services using Docker Compose.

### Setup Instructions

1.  **Prerequisites:** Docker and Docker Compose must be installed.
2.  **File Structure:** Create the directory structure as shown below.
3.  **Environment:** Create a `.env` file in the project root.
4.  **Run:** Execute `docker-compose up --build` from the root directory.
5.  **Test:**
    *   Access the API docs: `http://localhost:8000/docs`
    *   Use the endpoints provided in the API Gateway's documentation to test the authentication flow.

### Root Directory: `.env`

```dotenv
# .env

# This secret should be a long, randomly generated string (e.g., from `openssl rand -hex 32`)
# It MUST be the same for the API Gateway and the Auth Service for JWT validation.
JWT_SECRET_KEY=your-super-secret-key-that-is-at-least-32-bytes-long

# Service URLs for inter-service communication within the Docker network
AUTH_SERVICE_URL=http://auth-service:8001
PRODUCT_SERVICE_URL=http://product-service:8002
```

### Root Directory: `docker-compose.yml`

```yaml
# docker-compose.yml
version: '3.8'

services:
  api-gateway:
    build: ./services/api-gateway
    ports:
      - "8000:8000"
    env_file:
      - .env
    depends_on:
      - auth-service
    volumes:
      - ./services/api-gateway/app:/app
    command: uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

  auth-service:
    build: ./services/auth-service
    # No port mapping needed as it's only accessed internally
    # ports:
    #  - "8001:8001"
    env_file:
      - .env
    volumes:
      - ./services/auth-service/app:/app
    command: uvicorn app.main:app --host 0.0.0.0 --port 8001 --reload

# Add other services like product-service, postgres, redis here later
```

### Service: `auth-service`

#### `services/auth-service/Dockerfile`

```dockerfile
# services/auth-service/Dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# The port is defined in the docker-compose command
# EXPOSE 8001
```

#### `services/auth-service/requirements.txt`

```text
# services/auth-service/requirements.txt
fastapi==0.111.0
uvicorn[standard]==0.29.0
pydantic==2.7.1
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
pydantic-settings==2.2.1
```

#### `services/auth-service/app/config.py`

```python
# services/auth-service/app/config.py
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    """Loads environment variables for the application."""
    JWT_SECRET_KEY: str
    
    # Algorithm for JWT signing
    ALGORITHM: str = "HS256"
    # Token expiration time in minutes
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding='utf-8', extra='ignore')

settings = Settings()
```

#### `services/auth-service/app/main.py`

```python
# services/auth-service/app/main.py
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from . import security, schemas
from .config import settings

app = FastAPI(
    title="Authentication Service",
    description="Handles user authentication and JWT generation.",
    version="1.0.0"
)

# In-memory "database" for demonstration purposes.
# In a real application, this would be a PostgreSQL database.
fake_users_db = {
    "testuser": {
        "username": "testuser",
        "full_name": "Test User",
        "email": "test@example.com",
        "hashed_password": security.get_password_hash("password123"),
        "disabled": False,
    }
}

@app.post("/token", response_model=schemas.Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Authenticates a user and returns a JWT access token.
    """
    user = security.authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = security.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/validate", response_model=schemas.User)
async def validate_token(current_user: schemas.User = Depends(security.get_current_active_user)):
    """
    Validates a token and returns the user's data.
    This endpoint is called internally by the API Gateway.
    """
    return current_user
```

#### `services/auth-service/app/schemas.py`

```python
# services/auth-service/app/schemas.py
from pydantic import BaseModel
from typing import Optional

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

class User(BaseModel):
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    disabled: Optional[bool] = None

class UserInDB(User):
    hashed_password: str
```

#### `services/auth-service/app/security.py`

```python
# services/auth-service/app/security.py
from datetime import datetime, timedelta, timezone
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from .config import settings
from .schemas import User, UserInDB, TokenData

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token") # This URL is relative to the client

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)
    return None

def authenticate_user(db, username: str, password: str):
    user = get_user(db, username)
    if not user or not verify_password(password, user.hashed_password):
        return False
    return user

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    
    # In a real app, you'd fetch the user from the database here
    user = get_user(fake_users_db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user

async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

# This is a placeholder for the in-memory DB used in main.py
fake_users_db = {
    "testuser": {
        "username": "testuser",
        "full_name": "Test User",
        "email": "test@example.com",
        "hashed_password": get_password_hash("password123"),
        "disabled": False,
    }
}
```

### Service: `api-gateway`

#### `services/api-gateway/Dockerfile`

```dockerfile
# services/api-gateway/Dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# The port is defined in the docker-compose command
# EXPOSE 8000
```

#### `services/api-gateway/requirements.txt`

```text
# services/api-gateway/requirements.txt
fastapi==0.111.0
uvicorn[standard]==0.29.0
pydantic==2.7.1
httpx==0.27.0
pydantic-settings==2.2.1
python-jose[cryptography]==3.3.0
```

#### `services/api-gateway/app/config.py`

```python
# services/api-gateway/app/config.py
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    """Loads environment variables for the application."""
    AUTH_SERVICE_URL: str
    PRODUCT_SERVICE_URL: str
    JWT_SECRET_KEY: str
    ALGORITHM: str = "HS256"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding='utf-8', extra='ignore')

settings = Settings()
```

#### `services/api-gateway/app/main.py`

```python
# services/api-gateway/app/main.py
import httpx
from fastapi import FastAPI, Request, Response, Depends, HTTPException, status
from fastapi.routing import APIRoute
from .security import get_current_user
from .schemas import User

# Custom router class to add tags to all routes
class TaggedRoute(APIRoute):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.tags is None:
            self.tags = []
        self.tags.insert(0, "API Gateway")

app = FastAPI(
    title="API Gateway",
    description="The single entry point for all client requests.",
    version="1.0.0",
    route_class=TaggedRoute
)

# --- Authentication Routes ---
# These routes are proxied to the Auth Service
@app.post("/auth/token", tags=["Authentication"])
async def get_token(request: Request):
    """
    Proxies login requests to the Auth Service to get a JWT token.
    """
    from .services import auth_service
    return await auth_service.proxy_to_auth(request)

# --- Protected Routes ---
# These routes require a valid JWT and are proxied to downstream services
@app.get("/products/{product_id}", tags=["Products"])
async def get_product(
    product_id: int, 
    request: Request,
    current_user: User = Depends(get_current_user)
):
    """
    Example of a protected route. It first validates the user's token,
    then proxies the request to the Product Service.
    """
    # For this PoC, we'll just return a mock response.
    # In a real implementation, you would proxy to the Product Service:
    # from .services import product_service
    # return await product_service.proxy_to_product(request)
    
    return {
        "message": f"Access granted for user: {current_user.username}",
        "product_id": product_id,
        "product_name": "Sample Product",
        "note": "This is a mock response from the API Gateway."
    }

@app.get("/users/me", response_model=User, tags=["Users"])
async def read_users_me(current_user: User = Depends(get_current_user)):
    """
    A protected endpoint that returns the current user's data
    based on the provided JWT token.
    """
    return current_user
```

#### `services/api-gateway/app/security.py`

```python
# services/api-gateway/app/security.py
from fastapi import Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
import httpx

from .config import settings
from .schemas import User, TokenData

# This URL must match the one the client calls on the gateway
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

async def get_current_user(request: Request, token: str = Depends(oauth2_scheme)) -> User:
    """
    Decodes the JWT token locally for basic validation, but could also
    call the Auth service's /validate endpoint for full validation.
    This hybrid approach reduces latency for most requests.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        # If local decoding fails, we could optionally fall back to calling the auth service
        # for a full validation check, which might handle token revocation lists, etc.
        # For now, we just fail.
        raise credentials_exception

    # Here we just trust the username from the token.
    # A more secure pattern would be to pass the token to the auth service
    # to get the full, up-to-date user object.
    # For this example, we create a user object from the token data.
    user = User(username=token_data.username)
    if user is None:
        raise credentials_exception
    
    return user
```

#### `services/api-gateway/app/schemas.py`

```python
# services/api-gateway/app/schemas.py
from pydantic import BaseModel
from typing import Optional

class TokenData(BaseModel):
    username: Optional[str] = None

class User(BaseModel):
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    disabled: Optional[bool] = None
```

#### `services/api-gateway/app/services.py`

```python
# services/api-gateway/app/services.py
from fastapi import Request, HTTPException
import httpx
from .config import settings

async def _proxy_request(client: httpx.AsyncClient, request: Request):
    """Generic proxy helper function."""
    url = httpx.URL(path=request.url.path, query=request.url.query.encode("utf-8"))
    
    # Prepare the request to the downstream service
    rp_req = client.build_request(
        method=request.method,
        url=url,
        headers=request.headers.raw,
        content=await request.body(),
    )
    
    # Send the request
    try:
        rp_resp = await client.send(rp_req, stream=True)
    except httpx.ConnectError:
        raise HTTPException(status_code=503, detail="Service is unavailable.")

    # Return the response from the downstream service
    return httpx.Response(
        status_code=rp_resp.status_code,
        headers=rp_resp.headers,
        content=rp_resp.content,
    )

async def proxy_to_auth(request: Request):
    """Proxies a request to the Authentication Service."""
    async with httpx.AsyncClient(base_url=settings.AUTH_SERVICE_URL) as client:
        return await _proxy_request(client, request)

async def proxy_to_product(request: Request):
    """Proxies a request to the Product Service."""
    async with httpx.AsyncClient(base_url=settings.PRODUCT_SERVICE_URL) as client:
        return await _proxy_request(client, request)
```
✅ Streaming completed.