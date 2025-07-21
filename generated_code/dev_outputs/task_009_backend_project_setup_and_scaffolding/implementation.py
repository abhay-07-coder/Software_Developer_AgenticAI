Of course. As a Senior Full-Stack Software Developer AI Agent, I will now create the complete backend project scaffolding for a Node.js/Express application using TypeScript. The implementation will adhere to the highest standards of code quality, security, and maintainability.

## Architecture Overview

This project will be initialized with a layered architecture, which is a cornerstone of clean, maintainable, and scalable applications. This approach promotes separation of concerns and prepares the codebase for future expansion, such as integrating with databases or evolving into a microservices-based system.

-   **Presentation Layer (`api/`):** Contains all components related to handling HTTP requests and responses. This includes routes, controllers, and request/response validation schemas.
-   **Middleware Layer (`middleware/`):** Holds reusable middleware for tasks like logging, authentication, authorization, and centralized error handling.
-   **Configuration Layer (`config/`):** Manages all application configuration, primarily through environment variables, ensuring a clean separation between code and configuration.
-   **Utilities Layer (`utils/`):** Provides shared, cross-cutting utilities like logging instances.
-   **Server Entrypoint (`server.ts`, `app.ts`):** The `server.ts` file is responsible for starting the server and handling graceful shutdown, while `app.ts` composes the Express application by wiring together middleware and routes.

This structure ensures that each part of the application has a distinct responsibility, making it easier to develop, test, and maintain.

## Git Repository Initialization

To begin, create a new project directory and initialize a Git repository.

```bash
mkdir my-backend-project
cd my-backend-project
git init
```

## Setup Instructions

1.  **Prerequisites:**
    *   Node.js (v18.x or later)
    *   npm or yarn
    *   Docker (for containerized deployment)

2.  **Installation:**
    *   Clone the repository (or copy the files into your initialized directory).
    *   Install the dependencies:
        ```bash
        npm install
        ```

3.  **Environment Configuration:**
    *   Create a `.env` file in the root directory by copying the example:
        ```bash
        cp .env.example .env
        ```
    *   Modify the `.env` file with your desired settings (e.g., change `PORT`).

4.  **Running the Application:**
    *   **Development Mode (with hot-reloading):**
        ```bash
        npm run dev
        ```
    *   **Production Mode:**
        First, build the TypeScript code:
        ```bash
        npm run build
        ```
        Then, run the compiled JavaScript:
        ```bash
        npm start
        ```

5.  **Running with Docker:**
    *   Build and run the container using Docker Compose:
        ```bash
        docker-compose up --build
        ```
    The application will be available at `http://localhost:8080` (or the port specified in your `.env` file).

6.  **Accessing API and Documentation:**
    *   **Health Check:** `http://localhost:8080/api/v1/health`
    *   **API Documentation (Swagger):** `http://localhost:8080/api-docs`

## Project Structure

Here is the final folder structure for the project:

```
/
├── dist/
├── src/
│   ├── api/
│   │   └── v1/
│   │       ├── controllers/
│   │       │   └── health.controller.ts
│   │       ├── routes/
│   │       │   ├── health.route.ts
│   │       │   └── index.ts
│   │       └── swagger.ts
│   ├── config/
│   │   └── index.ts
│   ├── middleware/
│   │   ├── errorHandler.ts
│   │   └── requestLogger.ts
│   ├── utils/
│   │   └── logger.ts
│   ├── app.ts
│   └── server.ts
├── tests/
│   ├── integration/
│   │   └── health.test.ts
│   └── jest.setup.ts
├── .dockerignore
├── .env.example
├── .eslintrc.js
├── .gitignore
├── .prettierrc
├── Dockerfile
├── docker-compose.yml
├── jest.config.js
├── package.json
├── README.md
└── tsconfig.json
```

---

## Code Artifacts

### `package.json`

This file defines the project's dependencies, scripts, and metadata.

```json
{
  "name": "production-grade-backend",
  "version": "1.0.0",
  "description": "Production-grade Node.js backend scaffolding",
  "main": "dist/server.js",
  "scripts": {
    "start": "node dist/server.js",
    "dev": "nodemon src/server.ts",
    "build": "tsc",
    "test": "jest --verbose --runInBand",
    "test:watch": "jest --watch",
    "lint": "eslint . --ext .ts",
    "lint:fix": "eslint . --ext .ts --fix",
    "format": "prettier --write \"src/**/*.ts\" \"tests/**/*.ts\"",
    "prepare": "husky install"
  },
  "keywords": [
    "nodejs",
    "express",
    "typescript",
    "boilerplate"
  ],
  "author": "AI Agent",
  "license": "ISC",
  "dependencies": {
    "cors": "^2.8.5",
    "dotenv": "^16.3.1",
    "express": "^4.18.2",
    "express-rate-limit": "^7.1.5",
    "helmet": "^7.1.0",
    "pino": "^8.17.2",
    "swagger-jsdoc": "^6.2.8",
    "swagger-ui-express": "^5.0.0"
  },
  "devDependencies": {
    "@types/cors": "^2.8.17",
    "@types/express": "^4.17.21",
    "@types/jest": "^29.5.11",
    "@types/node": "^20.11.0",
    "@types/supertest": "^6.0.2",
    "@types/swagger-jsdoc": "^6.0.4",
    "@types/swagger-ui-express": "^4.1.6",
    "@typescript-eslint/eslint-plugin": "^6.18.1",
    "@typescript-eslint/parser": "^6.18.1",
    "eslint": "^8.56.0",
    "eslint-config-prettier": "^9.1.0",
    "eslint-plugin-prettier": "^5.1.3",
    "husky": "^8.0.0",
    "jest": "^29.7.0",
    "nodemon": "^3.0.2",
    "pino-pretty": "^10.3.1",
    "prettier": "^3.2.2",
    "supertest": "^6.3.4",
    "ts-jest": "^29.1.1",
    "ts-node": "^10.9.2",
    "typescript": "^5.3.3"
  }
}
```

### `tsconfig.json`

TypeScript compiler configuration.

```json
{
  "compilerOptions": {
    "target": "ES2020",
    "module": "commonjs",
    "rootDir": "./src",
    "outDir": "./dist",
    "esModuleInterop": true,
    "forceConsistentCasingInFileNames": true,
    "strict": true,
    "skipLibCheck": true,
    "baseUrl": ".",
    "paths": {
      "@/*": ["src/*"]
    }
  },
  "include": ["src/**/*"],
  "exclude": ["node_modules", "tests"]
}
```

### `.eslintrc.js`

ESLint configuration for code linting.

```javascript
module.exports = {
  parser: '@typescript-eslint/parser',
  extends: [
    'plugin:@typescript-eslint/recommended',
    'prettier',
    'plugin:prettier/recommended',
  ],
  parserOptions: {
    ecmaVersion: 2020,
    sourceType: 'module',
  },
  rules: {
    '@typescript-eslint/no-unused-vars': ['error', { 'argsIgnorePattern': '^_' }],
    '@typescript-eslint/explicit-function-return-type': 'warn',
    '@typescript-eslint/no-explicit-any': 'warn',
  },
};
```

### `.prettierrc`

Prettier configuration for code formatting.

```json
{
  "semi": true,
  "trailingComma": "all",
  "singleQuote": true,
  "printWidth": 80,
  "tabWidth": 2
}
```

### `.gitignore`

Specifies files to be ignored by Git.

```
# Dependencies
/node_modules

# Build artifacts
/dist

# Logs
logs
*.log
npm-debug.log*
yarn-debug.log*
yarn-error.log*

# Environment variables
.env
.env.local
.env.development.local
.env.test.local
.env.production.local

# IDEs and editors
.idea
.vscode
*.suo
*.ntvs*
*.njsproj
*.sln
*.sw?

# OS generated files
.DS_Store
Thumbs.db
```

### `.env.example`

Example environment variables file.

```
# Application Configuration
NODE_ENV=development
PORT=8080

# Rate Limiting
# Max 100 requests per 15 minutes per IP
RATE_LIMIT_WINDOW_MS=900000
RATE_LIMIT_MAX_REQUESTS=100
```

### `src/config/index.ts`

Loads and exports environment variables with type safety and defaults.

```typescript
import dotenv from 'dotenv';

// Load environment variables from .env file
dotenv.config();

const config = {
  env: process.env.NODE_ENV || 'development',
  port: process.env.PORT || 8080,
  rateLimit: {
    windowMs: process.env.RATE_LIMIT_WINDOW_MS
      ? parseInt(process.env.RATE_LIMIT_WINDOW_MS, 10)
      : 15 * 60 * 1000, // 15 minutes
    max: process.env.RATE_LIMIT_MAX_REQUESTS
      ? parseInt(process.env.RATE_LIMIT_MAX_REQUESTS, 10)
      : 100, // max 100 requests per windowMs
  },
};

export default config;
```

### `src/utils/logger.ts`

Configures the Pino logger for high-performance, structured logging.

```typescript
import pino from 'pino';
import config from '@/config';

const logger = pino({
  level: config.env === 'development' ? 'debug' : 'info',
  // Pretty print in development for better readability
  transport:
    config.env === 'development'
      ? {
          target: 'pino-pretty',
          options: {
            colorize: true,
            translateTime: 'SYS:standard',
            ignore: 'pid,hostname',
          },
        }
      : undefined,
});

export default logger;
```

### `src/middleware/requestLogger.ts`

Middleware to log every incoming HTTP request.

```typescript
import { Request, Response, NextFunction } from 'express';
import logger from '@/utils/logger';

export const requestLogger = (
  req: Request,
  _res: Response,
  next: NextFunction,
): void => {
  logger.info(
    {
      method: req.method,
      url: req.originalUrl,
      ip: req.ip,
      userAgent: req.get('User-Agent'),
    },
    'Incoming request',
  );
  next();
};
```

### `src/middleware/errorHandler.ts`

Centralized error handling middleware. Catches all errors and sends a standardized JSON response.

```typescript
import { Request, Response, NextFunction } from 'express';
import logger from '@/utils/logger';

interface AppError extends Error {
  statusCode?: number;
  isOperational?: boolean;
}

export const errorHandler = (
  err: AppError,
  _req: Request,
  res: Response,
  // eslint-disable-next-line @typescript-eslint/no-unused-vars
  _next: NextFunction,
): void => {
  const statusCode = err.statusCode || 500;
  const message = err.isOperational ? err.message : 'Internal Server Error';

  // Log the error for debugging purposes
  logger.error(err, 'An error occurred');

  res.status(statusCode).json({
    status: 'error',
    statusCode,
    message,
  });
};
```

### `src/api/v1/controllers/health.controller.ts`

Controller for the health check endpoint.

```typescript
import { Request, Response } from 'express';

/**
 * @description Handles the health check request.
 * @param {Request} _req - The Express request object.
 * @param {Response} res - The Express response object.
 * @returns {void}
 */
export const checkHealth = (_req: Request, res: Response): void => {
  const healthCheck = {
    uptime: process.uptime(),
    message: 'OK',
    timestamp: Date.now(),
  };

  res.status(200).json(healthCheck);
};
```

### `src/api/v1/routes/health.route.ts`

Defines the route for the health check endpoint.

```typescript
import { Router } from 'express';
import { checkHealth } from '../controllers/health.controller';

const router = Router();

/**
 * @openapi
 * /api/v1/health:
 *   get:
 *     tags:
 *       - Health
 *     summary: Responds if the app is up and running
 *     responses:
 *       200:
 *         description: App is up and running
 *         content:
 *           application/json:
 *             schema:
 *               type: object
 *               properties:
 *                 uptime:
 *                   type: number
 *                   description: Server uptime in seconds.
 *                 message:
 *                   type: string
 *                   example: OK
 *                 timestamp:
 *                   type: number
 *                   description: Current server timestamp.
 */
router.get('/health', checkHealth);

export default router;
```

### `src/api/v1/routes/index.ts`

Aggregates all v1 routes into a single router.

```typescript
import { Router } from 'express';
import healthRouter from './health.route';

const router = Router();

// Mount all v1 routes
router.use(healthRouter);

export default router;
```

### `src/api/v1/swagger.ts`

Configuration for Swagger/OpenAPI documentation.

```typescript
import swaggerJsdoc from 'swagger-jsdoc';
import swaggerUi from 'swagger-ui-express';
import { Express } from 'express';
import config from '@/config';
import { version } from '../../../package.json';

const options: swaggerJsdoc.Options = {
  definition: {
    openapi: '3.0.0',
    info: {
      title: 'Production-Grade Backend API',
      version,
      description: 'API documentation for the backend service.',
    },
    servers: [
      {
        url: `http://localhost:${config.port}`,
        description: 'Development server',
      },
    ],
  },
  apis: ['./src/api/v1/routes/*.ts'],
};

const swaggerSpec = swaggerJsdoc(options);

export const setupSwagger = (app: Express): void => {
  app.use('/api-docs', swaggerUi.serve, swaggerUi.setup(swaggerSpec));
};
```

### `src/app.ts`

The main Express application setup file.

```typescript
import express, { Express, Request, Response, NextFunction } from 'express';
import cors from 'cors';
import helmet from 'helmet';
import rateLimit from 'express-rate-limit';
import config from '@/config';
import apiV1Router from '@/api/v1/routes';
import { requestLogger } from '@/middleware/requestLogger';
import { errorHandler } from '@/middleware/errorHandler';
import { setupSwagger } from '@/api/v1/swagger';

const app: Express = express();

// --- Core Middleware ---

// Enable Cross-Origin Resource Sharing
app.use(cors());

// Set various HTTP headers for security
app.use(helmet());

// Parse JSON bodies
app.use(express.json());

// Rate limiting to prevent abuse
const limiter = rateLimit({
  windowMs: config.rateLimit.windowMs,
  max: config.rateLimit.max,
  standardHeaders: true, // Return rate limit info in the `RateLimit-*` headers
  legacyHeaders: false, // Disable the `X-RateLimit-*` headers
});
app.use(limiter);

// Log incoming requests
app.use(requestLogger);

// --- API Routes ---

// Setup Swagger API documentation
setupSwagger(app);

// Mount API v1 routes
app.use('/api/v1', apiV1Router);

// --- Error Handling ---

// Handle 404 Not Found for any unhandled routes
app.use((_req: Request, res: Response) => {
  res.status(404).json({
    status: 'error',
    statusCode: 404,
    message: 'The requested resource was not found on this server.',
  });
});

// Centralized error handler middleware
app.use(errorHandler);

export default app;
```

### `src/server.ts`

The server entry point. It initializes and starts the HTTP server.

```typescript
import app from './app';
import config from './config';
import logger from './utils/logger';

const server = app.listen(config.port, () => {
  logger.info(`Server is running on port ${config.port} in ${config.env} mode`);
  logger.info(`API documentation available at http://localhost:${config.port}/api-docs`);
});

// Graceful shutdown
const signals = ['SIGTERM', 'SIGINT'];

const gracefulShutdown = (signal: string) => {
  process.on(signal, async () => {
    logger.info(`Received ${signal}, shutting down gracefully...`);
    server.close(() => {
      logger.info('HTTP server closed.');
      // Add any other cleanup logic here (e.g., database connections)
      process.exit(0);
    });
  });
};

signals.forEach((signal) => {
  gracefulShutdown(signal);
});
```

### `jest.config.js`

Jest test runner configuration.

```javascript
module.exports = {
  preset: 'ts-jest',
  testEnvironment: 'node',
  moduleNameMapper: {
    '^@/(.*)$': '<rootDir>/src/$1',
  },
  testMatch: ['<rootDir>/tests/**/*.test.ts'],
  setupFilesAfterEnv: ['<rootDir>/tests/jest.setup.ts'],
  collectCoverage: true,
  coverageDirectory: 'coverage',
  coverageReporters: ['text', 'lcov'],
};
```

### `tests/jest.setup.ts`

Setup file for Jest tests (e.g., for global mocks or environment setup).

```typescript
// This file is executed before each test file.
// You can use it for global setup, like mocking modules or setting up a test database.

// For example, you might want to silence the logger during tests
jest.mock('../src/utils/logger', () => ({
  info: jest.fn(),
  warn: jest.fn(),
  error: jest.fn(),
  debug: jest.fn(),
}));
```

### `tests/integration/health.test.ts`

Integration test for the health check endpoint.

```typescript
import request from 'supertest';
import app from '@/app';

describe('GET /api/v1/health', () => {
  it('should respond with a 200 status code and health information', async () => {
    const response = await request(app).get('/api/v1/health');

    expect(response.status).toBe(200);
    expect(response.body).toHaveProperty('uptime');
    expect(response.body).toHaveProperty('message', 'OK');
    expect(response.body).toHaveProperty('timestamp');
    expect(typeof response.body.uptime).toBe('number');
  });
});
```

### `Dockerfile`

A multi-stage Dockerfile for creating a lean, optimized production image.

```dockerfile
# ---- Base Stage ----
# Use a specific Node.js version for reproducibility
FROM node:18-alpine AS base
WORKDIR /usr/src/app
# Install dependencies needed for building native modules
RUN apk add --no-cache libc6-compat

# ---- Dependencies Stage ----
FROM base AS deps
# Copy package.json and package-lock.json
COPY package.json package-lock.json* ./
# Install production dependencies
RUN npm ci --only=production

# ---- Build Stage ----
FROM base AS build
# Copy package.json and package-lock.json
COPY package.json package-lock.json* ./
# Install all dependencies including devDependencies
RUN npm ci
# Copy source code
COPY . .
# Transpile TypeScript to JavaScript
RUN npm run build

# ---- Production Stage ----
FROM base AS production
# Set environment to production
ENV NODE_ENV=production
# Copy production dependencies from the 'deps' stage
COPY --from=deps /usr/src/app/node_modules ./node_modules
# Copy compiled code from the 'build' stage
COPY --from=build /usr/src/app/dist ./dist
# Copy package.json to be able to run 'npm start'
COPY package.json .

# Expose the application port
EXPOSE 8080

# The command to run the application
CMD ["npm", "start"]
```

### `.dockerignore`

Prevents unnecessary files from being copied into the Docker image.

```
node_modules
npm-debug.log
Dockerfile
.dockerignore
.git
.gitignore
.env
README.md
src/
tests/
coverage/
.eslintrc.js
.prettierrc
jest.config.js
tsconfig.json
```

### `docker-compose.yml`

Docker Compose file for easy local development and testing.

```yaml
version: '3.8'

services:
  backend:
    build:
      context: .
      dockerfile: Dockerfile
    ports:
      - "8080:8080"
    env_file:
      - .env
    volumes:
      # In development, you might want to mount the src directory for hot-reloading
      # But for this setup, we rely on the Docker build process.
      # For a dev setup with hot-reload, you'd use a different command and mount volumes.
      # e.g., command: npm run dev
      # volumes:
      #  - ./src:/usr/src/app/src
      #  - ./tests:/usr/src/app/tests
    restart: unless-stopped
```

### `README.md`

A basic README file for the project.

```markdown
# Production-Grade Backend Service

This repository contains the scaffolding for a production-grade backend service built with Node.js, Express, and TypeScript.

## Features

-   **TypeScript:** For type safety and improved developer experience.
-   **Layered Architecture:** Clear separation of concerns (API, Config, Middleware).
-   **Production-Ready Logging:** High-performance, structured logging with Pino.
-   **Robust Error Handling:** Centralized error handling middleware.
-   **Security:** Basic security with Helmet, CORS, and rate limiting.
-   **Configuration Management:** Environment-based configuration using `dotenv`.
-   **API Documentation:** Automated OpenAPI (Swagger) documentation.
-   **Testing:** Setup for unit and integration testing with Jest and Supertest.
-   **Linting & Formatting:** ESLint and Prettier for consistent code style.
-   **Containerization:** Multi-stage Dockerfile for lean production images and Docker Compose for local development.

## Getting Started

### Prerequisites

-   Node.js (v18.x or later)
-   npm (or yarn)
-   Docker

### Installation

1.  Clone the repository:
    ```bash
    git clone <repository-url>
    cd <repository-name>
    ```

2.  Install dependencies:
    ```bash
    npm install
    ```

3.  Create your environment file:
    ```bash
    cp .env.example .env
    ```
    Update `.env` with your desired configuration.

### Running the Application

**Development Mode (with hot-reloading):**

```bash
npm run dev
```

**Production Mode:**

```bash
# 1. Build the project
npm run build

# 2. Start the server
npm start
```

**Using Docker:**

```bash
docker-compose up --build
```

The application will be available at `http://localhost:8080` (or the port specified in your `.env` file).

### API Endpoints

-   **Health Check:** `GET /api/v1/health`
-   **API Documentation (Swagger):** `http://localhost:8080/api-docs`

### Scripts

-   `npm run dev`: Start the development server with `nodemon`.
-   `npm start`: Start the production server.
-   `npm run build`: Compile TypeScript to JavaScript.
-   `npm test`: Run all tests.
-   `npm run lint`: Lint the codebase.
-   `npm run format`: Format the codebase with Prettier.
```
✅ Streaming completed.