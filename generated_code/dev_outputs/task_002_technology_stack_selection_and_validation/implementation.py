## Project Context (Inferred from task_001)

Based on the dependency `task_001` (Project Requirements Definition), we infer the project is a **Real-time Collaborative Project Management Tool**.

### Key Functional Requirements:
-   User authentication and authorization.
-   Real-time updates for all collaborative actions (e.g., creating/updating tasks, adding comments).
-   Core project management features: workspaces, boards, lists, and tasks (cards).
-   RESTful API for client-server communication.
-   Scalable architecture to support a growing number of users and concurrent connections.

### Key Non-Functional Requirements:
-   **High Performance:** Low latency for API responses and real-time updates.
-   **Scalability:** The system must be able to scale horizontally to handle increased load.
-   **Security:** The application must be secure, protecting user data and preventing common vulnerabilities.
-   **Maintainability:** The codebase should be clean, well-documented, and easy to maintain and extend.
-   **Cost-Effectiveness:** The chosen technologies and infrastructure should offer a good balance between performance and cost.

These requirements form the basis for the technology stack selection and validation process outlined below.

## 1. Technology Stack Selection Rationale

This document outlines the chosen technology stack for the project, providing justification for each component based on the project requirements.

### 1.1. Backend: Python with FastAPI

*   **Framework**: **FastAPI**
*   **Justification**:
    *   **Performance**: FastAPI is one of the fastest Python web frameworks available, with performance comparable to Node.js and Go, thanks to its foundation on Starlette (for web parts) and Pydantic (for data parts).
    *   **Asynchronous Support**: Built-in `async`/`await` support is crucial for handling high-concurrency I/O operations, such as managing many simultaneous database connections and WebSocket connections, which is a core requirement for our real-time application.
    *   **Developer Experience**: Automatic, interactive API documentation (Swagger UI and ReDoc) accelerates development and testing. The use of Python type hints for validation and serialization reduces boilerplate and catches errors early.
    *   **Ecosystem**: It leverages the vast and mature Python ecosystem for libraries in data science, security, and more.

### 1.2. Frontend: React with TypeScript

*   **Framework**: **React**
*   **Language**: **TypeScript**
*   **Justification**:
    *   **Component-Based Architecture**: React's model promotes the creation of reusable UI components, leading to a more maintainable and scalable frontend codebase.
    *   **Rich Ecosystem**: A vast ecosystem of libraries, tools (e.g., Redux, React Router), and a strong community ensures that we can solve complex problems without reinventing the wheel.
    *   **Performance**: The Virtual DOM allows for efficient UI updates, which is critical for a responsive user experience, especially when handling real-time data from WebSockets.
    *   **Type Safety**: TypeScript adds static typing to JavaScript, which significantly reduces runtime errors, improves code quality, and makes large-scale applications easier to refactor and maintain.

### 1.3. Database: PostgreSQL

*   **Database**: **PostgreSQL**
*   **Justification**:
    *   **Reliability and Robustness**: PostgreSQL is a battle-tested, open-source object-relational database system known for its reliability, data integrity, and correctness.
    *   **Advanced Features**: It supports advanced data types like `JSONB` (for storing flexible, unstructured data within a relational model), full-text search, and a wide array of powerful indexing options. This is perfect for storing task details or user preferences.
    *   **Scalability**: It has strong support for replication and connection pooling, allowing it to scale effectively for read-heavy workloads.
    *   **Community & Extensions**: A vibrant community and powerful extensions like PostGIS (for geospatial data) and TimescaleDB (for time-series data) make it a versatile choice for future needs.

### 1.4. Real-time Communication: WebSockets

*   **Technology**: **WebSockets**
*   **Justification**:
    *   **Bidirectional Communication**: WebSockets provide a persistent, full-duplex communication channel over a single TCP connection. This is essential for our real-time collaboration features, allowing the server to push updates to clients instantly without waiting for a client request.
    *   **Low Latency**: By eliminating the overhead of repeated HTTP requests (as in polling), WebSockets significantly reduce latency, leading to a smoother user experience.
    *   **Framework Support**: Both FastAPI on the backend and modern frontend libraries have excellent, mature support for WebSockets.

### 1.5. Caching: Redis

*   **Technology**: **Redis**
*   **Justification**:
    *   **Performance**: Redis is an extremely fast in-memory key-value store, ideal for caching frequently accessed data (e.g., user sessions, hot board data) to reduce database load and improve API response times.
    *   **Versatility**: Beyond simple caching, Redis can be used as a message broker for pub/sub systems, which can help in scaling our WebSocket layer across multiple server instances.

### 1.6. Containerization & Deployment: Docker & AWS

*   **Containerization**: **Docker**
*   **Cloud Provider**: **Amazon Web Services (AWS)**
*   **Justification**:
    *   **Consistency**: Docker ensures that our application runs the same way in development, testing, and production environments, eliminating "it works on my machine" issues.
    *   **Scalability & Orchestration**: Docker containers are the standard unit of deployment for modern orchestration platforms like Kubernetes (available as a managed service via **AWS EKS**). This provides a clear path to horizontal scaling and high availability.
    *   **Managed Services**: AWS offers a comprehensive suite of managed services that align perfectly with our stack:
        *   **Amazon RDS for PostgreSQL**: Managed relational database service.
        *   **Amazon ElastiCache for Redis**: Managed caching service.
        *   **Amazon EKS (or ECS)**: Managed container orchestration.
        *   **AWS Application Load Balancer**: For distributing traffic and handling sticky sessions for WebSockets.

## 2. Licensing and Cost Implications

*   **Core Technologies**: The chosen core technologies (Python, FastAPI, React, TypeScript, PostgreSQL, Redis, Docker) are all **open-source** and free to use, with permissive licenses (MIT, BSD, etc.). This means there are no direct licensing fees.
*   **Cloud Costs**: The primary cost driver will be the cloud infrastructure on AWS. Costs will be based on usage of services like EKS/ECS, RDS, ElastiCache, and data transfer. A "pay-as-you-go" model provides flexibility.
*   **Cost Management**: We can manage costs effectively by:
    *   Starting with smaller instance sizes and scaling up as needed.
    *   Leveraging AWS Savings Plans or Reserved Instances for predictable workloads.
    *   Implementing auto-scaling policies to match resources to demand.
    *   Monitoring usage closely with AWS Cost Explorer and setting up billing alerts.

## 3. Proof-of-Concept (PoC) Architecture

The PoC will validate the core technology stack by implementing a single, end-to-end feature: **creating a task and seeing it appear in real-time on all connected clients.**

The architecture is as follows:
1.  **Frontend (React)**: A simple UI with a form to create a task and a list to display existing tasks. It establishes a WebSocket connection on load.
2.  **Backend (FastAPI)**:
    *   Exposes a REST endpoint (`POST /api/v1/tasks`) to create a new task. This endpoint is protected and requires a JWT.
    *   Exposes a simple `POST /token` endpoint to issue a dummy JWT for the PoC.
    *   Exposes a WebSocket endpoint (`/ws/{client_id}`).
    *   When a task is created via the REST endpoint, it's saved to the **PostgreSQL** database.
    *   After saving, the backend broadcasts the new task data to all connected clients via the WebSocket manager.
3.  **Database (PostgreSQL)**: Persists the tasks.
4.  **Docker Compose**: Orchestrates the `frontend`, `backend`, and `db` services for local development and validation.



## 4. PoC Setup and Deployment Instructions

### Prerequisites
-   Docker and Docker Compose installed on your local machine.

### Directory Structure

The PoC is organized into the following directory structure:

```
/project-poc
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   ├── endpoints/
│   │   │   │   ├── auth.py
│   │   │   │   └── tasks.py
│   │   │   └── ws.py
│   │   ├── core/
│   │   │   └── config.py
│   │   ├── crud/
│   │   │   └── crud_task.py
│   │   ├── db/
│   │   │   ├── base.py
│   │   │   └── session.py
│   │   ├── models/
│   │   │   └── task.py
│   │   ├── schemas/
│   │   │   ├── task.py
│   │   │   └── token.py
│   │   ├── security.py
│   │   └── main.py
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/
│   ├── public/
│   │   └── index.html
│   ├── src/
│   │   ├── App.tsx
│   │   ├── components/
│   │   │   └── TaskManager.tsx
│   │   ├── index.css
│   │   └── index.tsx
│   ├── Dockerfile
│   ├── package.json
│   └── tsconfig.json
└── docker-compose.yml
```

### Running the PoC

1.  **Clone the repository / Create the files:** Create the files and directories as specified in the code artifacts below.
2.  **Navigate to the root directory:**
    ```bash
    cd project-poc
    ```
3.  **Build and run the services using Docker Compose:**
    ```bash
    docker-compose up --build
    ```
4.  **Access the application:**
    *   **Frontend Application**: Open your browser and go to `http://localhost:3000`.
    *   **Backend API Docs**: Open your browser and go to `http://localhost:8000/docs`.

### How to Validate

1.  Open `http://localhost:3000` in two separate browser windows side-by-side.
2.  You will see an empty task list and a form to add a new task.
3.  In one window, type a task title (e.g., "Validate tech stack") and click "Add Task".
4.  Observe that the new task instantly appears in the task lists of **both** browser windows without needing a page refresh. This confirms the end-to-end flow from React -> FastAPI (REST) -> PostgreSQL -> FastAPI (WebSocket) -> React is working correctly.

---

## Code Artifacts

### `docker-compose.yml`
```yaml
version: '3.8'

services:
  db:
    image: postgres:15-alpine
    volumes:
      - postgres_data:/var/lib/postgresql/data/
    environment:
      - POSTGRES_USER=pocuser
      - POSTGRES_PASSWORD=pocpassword
      - POSTGRES_DB=pocdb
    ports:
      - "5432:5432"
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U pocuser -d pocdb"]
      interval: 10s
      timeout: 5s
      retries: 5

  backend:
    build: ./backend
    command: uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
    volumes:
      - ./backend:/app
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://pocuser:pocpassword@db/pocdb
      - SECRET_KEY=09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7
      - ALGORITHM=HS256
      - ACCESS_TOKEN_EXPIRE_MINUTES=30
    depends_on:
      db:
        condition: service_healthy

  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    volumes:
      - ./frontend/src:/app/src
    ports:
      - "3000:3000"
    environment:
      - REACT_APP_API_URL=http://localhost:8000
      - REACT_APP_WS_URL=ws://localhost:8000
    depends_on:
      - backend

volumes:
  postgres_data:
```

### `backend/requirements.txt`
```txt
fastapi==0.111.0
uvicorn[standard]==0.29.0
sqlalchemy==2.0.30
psycopg2-binary==2.9.9
pydantic-settings==2.2.1
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
python-multipart==0.0.9
```

### `backend/Dockerfile`
```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Set environment variables to prevent buffering
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# The command to run the application will be provided by docker-compose
# For standalone usage, you would add:
# CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### `backend/app/core/config.py`
```python
import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'

settings = Settings()
```

### `backend/app/db/session.py`
```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

# Create a synchronous engine
engine = create_engine(settings.DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
```

### `backend/app/db/base.py`
```python
from sqlalchemy.orm import declarative_base

Base = declarative_base()
```

### `backend/app/models/task.py`
```python
from sqlalchemy import Column, Integer, String
from app.db.base import Base

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
```

### `backend/app/schemas/task.py`
```python
from pydantic import BaseModel

class TaskBase(BaseModel):
    title: str

class TaskCreate(TaskBase):
    pass

class Task(TaskBase):
    id: int

    class Config:
        from_attributes = True
```

### `backend/app/schemas/token.py`
```python
from pydantic import BaseModel

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None
```

### `backend/app/crud/crud_task.py`
```python
from sqlalchemy.orm import Session
from app.models.task import Task
from app.schemas.task import TaskCreate

def get_tasks(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Task).offset(skip).limit(limit).all()

def create_task(db: Session, task: TaskCreate):
    db_task = Task(title=task.title)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task
```

### `backend/app/security.py`
```python
from datetime import datetime, timedelta, timezone
from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from app.core.config import settings
from app.db.session import SessionLocal
from app.schemas.token import TokenData

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Dummy user database for PoC
fake_users_db = {"testuser": {"password": "testpassword"}}

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    # In a real app, you would fetch the user from the DB here
    if token_data.username not in fake_users_db:
        raise credentials_exception
    return token_data.username
```

### `backend/app/api/ws.py`
```python
import json
from typing import List
from fastapi import APIRouter, WebSocket, WebSocketDisconnect

router = APIRouter()

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

manager = ConnectionManager()

@router.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int):
    await manager.connect(websocket)
    try:
        while True:
            # We are only broadcasting, not receiving messages from clients in this PoC
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)
```

### `backend/app/api/endpoints/auth.py`
```python
from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.core.config import settings
from app.schemas.token import Token
from app.security import create_access_token, fake_users_db

router = APIRouter()

@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    # In a real app, you'd verify the password hash
    user = fake_users_db.get(form_data.username)
    if not user or user.get("password") != form_data.password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": form_data.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
```

### `backend/app/api/endpoints/tasks.py`
```python
import json
from typing import List, Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import ws
from app.db.session import SessionLocal
from app.security import get_current_user

router = APIRouter()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=List[schemas.Task])
def read_tasks(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    tasks = crud.crud_task.get_tasks(db, skip=skip, limit=limit)
    return tasks

@router.post("/", response_model=schemas.Task)
async def create_task(
    task: schemas.TaskCreate,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    db_task = crud.crud_task.create_task(db=db, task=task)
    
    # Broadcast the new task to all connected WebSocket clients
    message = {
        "type": "new_task",
        "payload": {"id": db_task.id, "title": db_task.title}
    }
    await ws.manager.broadcast(json.dumps(message))
    
    return db_task
```

### `backend/app/main.py`
```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.db import base, session
from app.api.endpoints import tasks, auth
from app.api import ws

# Create database tables
base.Base.metadata.create_all(bind=session.engine)

app = FastAPI(title="Project Management PoC API")

# CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Allows frontend to connect
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers
app.include_router(auth.router, prefix="/token", tags=["auth"])
app.include_router(tasks.router, prefix="/api/v1/tasks", tags=["tasks"])
app.include_router(ws.router)

@app.get("/health")
def health_check():
    return {"status": "ok"}
```

### `frontend/package.json`
```json
{
  "name": "frontend",
  "version": "0.1.0",
  "private": true,
  "dependencies": {
    "@testing-library/jest-dom": "^5.17.0",
    "@testing-library/react": "^13.4.0",
    "@testing-library/user-event": "^13.5.0",
    "@types/jest": "^27.5.2",
    "@types/node": "^16.18.97",
    "@types/react": "^18.3.2",
    "@types/react-dom": "^18.3.0",
    "axios": "^1.7.2",
    "react": "^18.3.1",
    "react-dom": "^18.3.1",
    "react-scripts": "5.0.1",
    "typescript": "^4.9.5",
    "web-vitals": "^2.1.4"
  },
  "scripts": {
    "start": "react-scripts start",
    "build": "react-scripts build",
    "test": "react-scripts test",
    "eject": "react-scripts eject"
  },
  "eslintConfig": {
    "extends": [
      "react-app",
      "react-app/jest"
    ]
  },
  "browserslist": {
    "production": [
      ">0.2%",
      "not dead",
      "not op_mini all"
    ],
    "development": [
      "last 1 chrome version",
      "last 1 firefox version",
      "last 1 safari version"
    ]
  }
}
```

### `frontend/tsconfig.json`
```json
{
  "compilerOptions": {
    "target": "es5",
    "lib": [
      "dom",
      "dom.iterable",
      "esnext"
    ],
    "allowJs": true,
    "skipLibCheck": true,
    "esModuleInterop": true,
    "allowSyntheticDefaultImports": true,
    "strict": true,
    "forceConsistentCasingInFileNames": true,
    "noFallthroughCasesInSwitch": true,
    "module": "esnext",
    "moduleResolution": "node",
    "resolveJsonModule": true,
    "isolatedModules": true,
    "noEmit": true,
    "jsx": "react-jsx"
  },
  "include": [
    "src"
  ]
}
```

### `frontend/Dockerfile`
```dockerfile
# Stage 1: Build the React application
FROM node:18-alpine as build

WORKDIR /app

COPY package.json ./
COPY package-lock.json ./
RUN npm install

COPY . ./
RUN npm run build

# Stage 2: Serve the application using Nginx
FROM nginx:1.25-alpine

# Copy the built assets from the build stage
COPY --from=build /app/build /usr/share/nginx/html

# When the container starts, nginx will serve the files from /usr/share/nginx/html
# The default nginx config is sufficient for this PoC
EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
```

### `frontend/src/index.css`
```css
body {
  margin: 0;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen',
    'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue',
    sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  background-color: #f4f5f7;
  color: #172b4d;
}

code {
  font-family: source-code-pro, Menlo, Monaco, Consolas, 'Courier New',
    monospace;
}
```

### `frontend/src/index.tsx`
```typescript
import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import App from './App';

const root = ReactDOM.createRoot(
  document.getElementById('root') as HTMLElement
);
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
```

### `frontend/src/App.tsx`
```typescript
import React from 'react';
import TaskManager from './components/TaskManager';
import './App.css';

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <h1>Real-time Project Management PoC</h1>
      </header>
      <main>
        <TaskManager />
      </main>
    </div>
  );
}

// Basic styling for the App component
const styles = `
.App {
  text-align: center;
}

.App-header {
  background-color: #0052cc;
  padding: 20px;
  color: white;
  margin-bottom: 2rem;
}

main {
  display: flex;
  justify-content: center;
}
`;

const styleSheet = document.createElement("style");
styleSheet.innerText = styles;
document.head.appendChild(styleSheet);

export default App;
```

### `frontend/src/components/TaskManager.tsx`
```typescript
import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';
const WS_URL = process.env.REACT_APP_WS_URL || 'ws://localhost:8000';

interface Task {
    id: number;
    title: string;
}

const TaskManager: React.FC = () => {
    const [tasks, setTasks] = useState<Task[]>([]);
    const [newTaskTitle, setNewTaskTitle] = useState('');
    const [error, setError] = useState<string | null>(null);
    const [token, setToken] = useState<string | null>(null);
    const ws = useRef<WebSocket | null>(null);

    // 1. Authenticate and fetch initial tasks on component mount
    useEffect(() => {
        const authenticateAndFetch = async () => {
            try {
                // For PoC, we use hardcoded credentials to get a token
                const formData = new URLSearchParams();
                formData.append('username', 'testuser');
                formData.append('password', 'testpassword');

                const tokenResponse = await axios.post(`${API_URL}/token`, formData);
                const accessToken = tokenResponse.data.access_token;
                setToken(accessToken);

                // Fetch initial tasks
                const tasksResponse = await axios.get(`${API_URL}/api/v1/tasks`, {
                    headers: { Authorization: `Bearer ${accessToken}` }
                });
                setTasks(tasksResponse.data);
                setError(null);
            } catch (err) {
                console.error("Authentication or fetch error:", err);
                setError("Failed to authenticate or fetch tasks.");
            }
        };

        authenticateAndFetch();
    }, []);

    // 2. Setup WebSocket connection
    useEffect(() => {
        // Don't connect until we have tasks (and thus a token)
        if (tasks.length === 0 && !error) return;

        const clientId = Date.now(); // Simple unique ID for the client
        ws.current = new WebSocket(`${WS_URL}/ws/${clientId}`);

        ws.current.onopen = () => console.log("WebSocket connected");
        ws.current.onclose = () => console.log("WebSocket disconnected");

        ws.current.onmessage = (event) => {
            const message = JSON.parse(event.data);
            if (message.type === 'new_task') {
                setTasks(prevTasks => [...prevTasks, message.payload]);
            }
        };

        // Cleanup on component unmount
        return () => {
            ws.current?.close();
        };
    }, [tasks.length, error]); // Rerun if initial fetch succeeds or fails

    const handleAddTask = async (e: React.FormEvent) => {
        e.preventDefault();
        if (!newTaskTitle.trim() || !token) return;

        try {
            await axios.post(
                `${API_URL}/api/v1/tasks`,
                { title: newTaskTitle },
                { headers: { Authorization: `Bearer ${token}` } }
            );
            // No need to update state here, WebSocket will handle it
            setNewTaskTitle('');
            setError(null);
        } catch (err) {
            console.error("Failed to add task:", err);
            setError("Failed to add task. Your session might have expired.");
        }
    };

    return (
        <div style={styles.container}>
            <h2>Tasks</h2>
            {error && <p style={styles.error}>{error}</p>}
            <ul style={styles.taskList}>
                {tasks.map(task => (
                    <li key={task.id} style={styles.taskItem}>{task.title}</li>
                ))}
            </ul>
            <form onSubmit={handleAddTask} style={styles.form}>
                <input
                    type="text"
                    value={newTaskTitle}
                    onChange={(e) => setNewTaskTitle(e.target.value)}
                    placeholder="Enter a new task title"
                    style={styles.input}
                />
                <button type="submit" style={styles.button}>Add Task</button>
            </form>
        </div>
    );
};

// Basic inline styles for the component
const styles = {
    container: {
        backgroundColor: '#ffffff',
        padding: '20px',
        borderRadius: '3px',
        boxShadow: '0 1px 0 rgba(9,30,66,.25)',
        width: '400px',
    },
    taskList: {
        listStyle: 'none',
        padding: 0,
        margin: 0,
        marginBottom: '1rem',
    },
    taskItem: {
        backgroundColor: '#f4f5f7',
        borderRadius: '3px',
        padding: '10px',
        marginBottom: '8px',
        textAlign: 'left' as const,
    },
    form: {
        display: 'flex',
    },
    input: {
        flexGrow: 1,
        padding: '8px',
        border: '2px solid #dfe1e6',
        borderRadius: '3px',
        marginRight: '8px',
    },
    button: {
        backgroundColor: '#5aac44',
        color: 'white',
        border: 'none',
        padding: '8px 12px',
        borderRadius: '3px',
        cursor: 'pointer',
    },
    error: {
        color: 'red',
        marginBottom: '1rem',
    }
};

export default TaskManager;
```
✅ Streaming completed.