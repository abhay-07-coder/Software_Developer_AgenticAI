## Architecture and Design Overview

This document outlines the setup for a production-grade React frontend application using Vite. The architecture is designed for scalability, maintainability, and performance, adhering to modern best practices.

### Core Technologies

*   **Framework**: React 18 with TypeScript for robust, type-safe development.
*   **Build Tool**: Vite for its extremely fast Hot Module Replacement (HMR) and optimized build process.
*   **State Management**: Redux Toolkit, the official, opinionated toolset for efficient Redux development. It simplifies store setup, eliminates boilerplate, and includes powerful tools like Immer for immutable updates and Reselect for memoized selectors.
*   **Routing**: React Router DOM (v6+), utilizing the latest data-driven APIs for declarative and powerful routing.
*   **API Communication**: Axios, a promise-based HTTP client, configured with a centralized instance for easy management of base URLs, interceptors for authentication tokens, and consistent error handling.
*   **Styling**: A combination of global CSS for base styles and a structure that supports CSS Modules or styled-components for component-level styling.
*   **Testing**: Vitest for a fast, Vite-native unit and integration testing experience, paired with React Testing Library for user-centric component testing.

### Folder Structure

The project follows a feature-based folder structure. This approach organizes code by functionality rather than by type (e.g., all components in one folder, all hooks in another). This improves scalability and makes it easier for developers to locate and work on related files.

-   **`src/api`**: Contains the configured Axios instance and functions for making API calls.
-   **`src/app`**: Houses the Redux Toolkit store configuration and typed hooks.
-   **`src/components`**: For shared, reusable UI components (e.g., `Button`, `Input`, `Layout`).
-   **`src/features`**: The core of the application. Each feature (e.g., `auth`, `products`) gets its own directory containing its specific components, slices, and API logic.
-   **`src/hooks`**: For custom, reusable React hooks.
-   **`src/pages`**: Top-level components that correspond to a specific route. These pages compose components from `src/components` and `src/features`.
-   **`src/routes`**: Centralized routing configuration.
-   **`src/styles`**: Global styles, CSS variables, and theme definitions.
-   **`src/types`**: Global TypeScript type definitions and interfaces.
-   **`src/utils`**: Utility functions that are not specific to any component or feature.

This structure ensures a clean separation of concerns and supports a growing codebase by keeping related logic colocated.

## Initial Project Setup

Follow these steps to create the project from scratch, install dependencies, and run the development server.

### 1. Initialize Git Repository

First, create a directory for your frontend project and initialize a Git repository.

```bash
mkdir frontend
cd frontend
git init
git branch -M main
```

### 2. Scaffold the Vite + React Project

Use `npm create` to scaffold a new React project with the TypeScript template. The `.` indicates the project should be created in the current directory.

```bash
# Make sure you are inside the 'frontend' directory
npm create vite@latest . -- --template react-ts
```

### 3. Install Dependencies

Install the core libraries for state management, routing, API calls, and testing.

```bash
# Core Application Libraries
npm install react-router-dom @reduxjs/toolkit react-redux axios

# Development Dependencies for Testing and Code Quality
npm install -D vitest @vitest/ui jsdom @testing-library/react @testing-library/jest-dom @testing-library/user-event eslint-plugin-react-hooks@next eslint-plugin-react-refresh prettier eslint-config-prettier eslint-plugin-prettier
```

### 4. Run the Development Server

After installation, you can start the local development server.

```bash
npm run dev
```

The application will be available at `http://localhost:5173` by default.

## Configuration Files

These files configure the build tools, TypeScript, linting, and formatting to ensure consistency and quality.

### `package.json`

This file lists all project dependencies and defines scripts for running, building, and testing the application.

```json
{
  "name": "frontend",
  "private": true,
  "version": "0.0.0",
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "tsc && vite build",
    "lint": "eslint . --ext ts,tsx --report-unused-disable-directives --max-warnings 0",
    "lint:fix": "eslint . --ext ts,tsx --fix",
    "format": "prettier --write \"**/*.{ts,tsx,json,css,md}\"",
    "preview": "vite preview",
    "test": "vitest",
    "test:ui": "vitest --ui",
    "test:coverage": "vitest run --coverage"
  },
  "dependencies": {
    "@reduxjs/toolkit": "^2.2.5",
    "axios": "^1.7.2",
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "react-redux": "^9.1.2",
    "react-router-dom": "^6.23.1"
  },
  "devDependencies": {
    "@testing-library/jest-dom": "^6.4.5",
    "@testing-library/react": "^15.0.7",
    "@testing-library/user-event": "^14.5.2",
    "@types/node": "^20.12.12",
    "@types/react": "^18.2.66",
    "@types/react-dom": "^18.2.22",
    "@typescript-eslint/eslint-plugin": "^7.2.0",
    "@typescript-eslint/parser": "^7.2.0",
    "@vitejs/plugin-react": "^4.2.1",
    "@vitest/ui": "^1.6.0",
    "eslint": "^8.57.0",
    "eslint-config-prettier": "^9.1.0",
    "eslint-plugin-prettier": "^5.1.3",
    "eslint-plugin-react-hooks": "next",
    "eslint-plugin-react-refresh": "^0.4.6",
    "jsdom": "^24.0.0",
    "prettier": "^3.2.5",
    "typescript": "^5.2.2",
    "vite": "^5.2.0",
    "vitest": "^1.6.0"
  }
}
```

### `vite.config.ts`

Vite configuration file. Here we set up path aliases for cleaner imports and a proxy to the backend API to avoid CORS issues during development.

```typescript
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import path from 'path';

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
  server: {
    port: 3000, // Frontend port
    proxy: {
      // Proxy API requests to the backend server
      '/api': {
        target: 'http://localhost:8000', // Your backend API URL
        changeOrigin: true,
        secure: false,
      },
    },
  },
});
```

### `vitest.config.ts`

Configuration for Vitest. It extends the Vite config and sets up the testing environment.

```typescript
import { defineConfig, mergeConfig } from 'vitest/config';
import viteConfig from './vite.config';

export default mergeConfig(
  viteConfig,
  defineZeneca({
    test: {
      globals: true,
      environment: 'jsdom',
      setupFiles: './src/setupTests.ts',
      // You can specify a coverage provider here
      coverage: {
        provider: 'v8',
        reporter: ['text', 'json', 'html'],
      },
    },
  }),
);
```

### `tsconfig.json`

TypeScript compiler options. We add `baseUrl` and `paths` to align with the Vite path aliases.

```json
{
  "compilerOptions": {
    "target": "ES2020",
    "useDefineForClassFields": true,
    "lib": ["ES2020", "DOM", "DOM.Iterable"],
    "module": "ESNext",
    "skipLibCheck": true,

    /* Bundler mode */
    "moduleResolution": "bundler",
    "allowImportingTsExtensions": true,
    "resolveJsonModule": true,
    "isolatedModules": true,
    "noEmit": true,
    "jsx": "react-jsx",

    /* Linting */
    "strict": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "noFallthroughCasesInSwitch": true,

    /* Path Aliases */
    "baseUrl": ".",
    "paths": {
      "@/*": ["src/*"]
    }
  },
  "include": ["src", "vite.config.ts", "vitest.config.ts"],
  "references": [{ "path": "./tsconfig.node.json" }]
}
```

### `.eslintrc.cjs`

ESLint configuration for enforcing code quality and style.

```javascript
module.exports = {
  root: true,
  env: { browser: true, es2020: true, node: true },
  extends: [
    'eslint:recommended',
    'plugin:@typescript-eslint/recommended',
    'plugin:react-hooks/recommended',
    'prettier',
  ],
  ignorePatterns: ['dist', '.eslintrc.cjs', 'vite.config.ts'],
  parser: '@typescript-eslint/parser',
  plugins: ['react-refresh', 'prettier'],
  rules: {
    'prettier/prettier': 'warn',
    'react-refresh/only-export-components': [
      'warn',
      { allowConstantExport: true },
    ],
    '@typescript-eslint/no-unused-vars': [
      'warn',
      { argsIgnorePattern: '^_', varsIgnorePattern: '^_' },
    ],
  },
};
```

### `.prettierrc`

Prettier configuration for consistent code formatting.

```json
{
  "semi": true,
  "trailingComma": "all",
  "singleQuote": true,
  "printWidth": 80,
  "tabWidth": 2
}
```

### `.env.example`

Example environment variables file. Developers should copy this to `.env` for their local setup. **Never commit `.env` files to version control.**

```env
# The base URL for the backend API
VITE_API_BASE_URL=http://localhost:8000/api/v1
```

## Application Source Code

This section contains the core logic of the application, including the entry point, routing, state management, and example components.

### `src/main.tsx`

The main entry point of the application. It sets up the Redux store and the router.

```typescript
import React from 'react';
import ReactDOM from 'react-dom/client';
import { Provider } from 'react-redux';
import { RouterProvider } from 'react-router-dom';

import { store } from '@/app/store';
import router from '@/routes';
import '@/styles/index.css';

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <Provider store={store}>
      <RouterProvider router={router} />
    </Provider>
  </React.StrictMode>,
);
```

### `src/routes/index.tsx`

Centralized routing configuration using `react-router-dom`.

```typescript
import { createBrowserRouter } from 'react-router-dom';

import App from '@/App';
import HomePage from '@/pages/HomePage';
import NotFoundPage from '@/pages/NotFoundPage';

const router = createBrowserRouter([
  {
    path: '/',
    element: <App />,
    errorElement: <NotFoundPage />,
    children: [
      {
        index: true,
        element: <HomePage />,
      },
      // Add other routes here, e.g.,
      // {
      //   path: 'login',
      //   element: <LoginPage />,
      // },
    ],
  },
]);

export default router;
```

### `src/App.tsx`

The root component that renders the main layout.

```typescript
import Layout from '@/components/Layout';

function App() {
  return <Layout />;
}

export default App;
```

### `src/components/Layout.tsx`

A shared layout component containing a header, main content area, and footer. The `Outlet` from React Router renders the matched child route.

```typescript
import { Outlet } from 'react-router-dom';
import { useAppDispatch, useAppSelector } from '@/app/hooks';
import { toggleTheme, selectTheme } from '@/features/theme/themeSlice';

const Layout = () => {
  const dispatch = useAppDispatch();
  const currentTheme = useAppSelector(selectTheme);

  const handleThemeToggle = () => {
    dispatch(toggleTheme());
  };

  return (
    <div className={`theme-${currentTheme}`}>
      <div className="app-container">
        <header className="app-header">
          <h1>Frontend Application</h1>
          <button onClick={handleThemeToggle}>
            Switch to {currentTheme === 'light' ? 'Dark' : 'Light'} Mode
          </button>
        </header>
        <main className="app-main">
          <Outlet />
        </main>
        <footer className="app-footer">
          <p>&copy; {new Date().getFullYear()} - Production-Ready App</p>
        </footer>
      </div>
    </div>
  );
};

export default Layout;
```

### `src/pages/HomePage.tsx`

An example page component for the home route.

```typescript
const HomePage = () => {
  return (
    <div>
      <h2>Welcome to the Home Page</h2>
      <p>This is the main content area of your application.</p>
      <p>
        The project is set up with Vite, React, TypeScript, Redux Toolkit, and
        React Router.
      </p>
    </div>
  );
};

export default HomePage;
```

### `src/pages/NotFoundPage.tsx`

A page to display when a route is not found (404).

```typescript
import { useRouteError, Link, isRouteErrorResponse } from 'react-router-dom';

const NotFoundPage = () => {
  const error = useRouteError();
  let errorMessage: string;

  if (isRouteErrorResponse(error)) {
    // error is type `ErrorResponse`
    errorMessage = `${error.status} ${error.statusText}`;
  } else if (error instanceof Error) {
    errorMessage = error.message;
  } else if (typeof error === 'string') {
    errorMessage = error;
  } else {
    console.error(error);
    errorMessage = 'Unknown error';
  }

  return (
    <div id="error-page">
      <h1>Oops!</h1>
      <p>Sorry, an unexpected error has occurred.</p>
      <p>
        <i>{errorMessage}</i>
      </p>
      <Link to="/">Go back to Home</Link>
    </div>
  );
};

export default NotFoundPage;
```

### `src/app/store.ts`

Redux Toolkit store configuration.

```typescript
import { configureStore } from '@reduxjs/toolkit';
import themeReducer from '@/features/theme/themeSlice';

export const store = configureStore({
  reducer: {
    theme: themeReducer,
    // Add other feature reducers here
  },
});

// Infer the `RootState` and `AppDispatch` types from the store itself
export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;
```

### `src/app/hooks.ts`

Typed versions of `useDispatch` and `useSelector` for use throughout the app.

```typescript
import { useDispatch, useSelector } from 'react-redux';
import type { RootState, AppDispatch } from './store';

// Use throughout your app instead of plain `useDispatch` and `useSelector`
export const useAppDispatch = useDispatch.withTypes<AppDispatch>();
export const useAppSelector = useSelector.withTypes<RootState>();
```

### `src/features/theme/themeSlice.ts`

An example Redux slice for managing the UI theme (light/dark mode).

```typescript
import { createSlice } from '@reduxjs/toolkit';
import type { RootState } from '@/app/store';

type Theme = 'light' | 'dark';

interface ThemeState {
  value: Theme;
}

const initialState: ThemeState = {
  value: 'light',
};

export const themeSlice = createSlice({
  name: 'theme',
  initialState,
  reducers: {
    toggleTheme: (state) => {
      state.value = state.value === 'light' ? 'dark' : 'light';
    },
  },
});

export const { toggleTheme } = themeSlice.actions;

export const selectTheme = (state: RootState) => state.theme.value;

export default themeSlice.reducer;
```

### `src/api/axios.ts`

A pre-configured Axios instance for making API requests.

```typescript
import axios from 'axios';

const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Optional: Add a request interceptor to include the auth token
apiClient.interceptors.request.use(
  (config) => {
    // Example: Get token from local storage or state management
    const token = localStorage.getItem('authToken');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  },
);

// Optional: Add a response interceptor for global error handling
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    // Example: Handle 401 Unauthorized errors by redirecting to login
    if (error.response && error.response.status === 401) {
      // window.location.href = '/login';
      console.error('Unauthorized, redirecting to login...');
    }
    return Promise.reject(error);
  },
);

export default apiClient;
```

### `src/styles/index.css`

Global stylesheet with CSS variables for theming.

```css
/* Global styles and CSS variables */
:root {
  --font-family: Inter, system-ui, Avenir, Helvetica, Arial, sans-serif;
  --line-height: 1.5;
  --font-weight: 400;

  --color-scheme: light dark;

  font-synthesis: none;
  text-rendering: optimizeLegibility;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

/* Light theme variables */
.theme-light {
  --background-color: #ffffff;
  --text-color: #213547;
  --header-bg: #f8f9fa;
  --footer-bg: #f1f3f5;
  --button-bg: #646cff;
  --button-text: #ffffff;
}

/* Dark theme variables */
.theme-dark {
  --background-color: #242424;
  --text-color: rgba(255, 255, 255, 0.87);
  --header-bg: #1a1a1a;
  --footer-bg: #1a1a1a;
  --button-bg: #747bff;
  --button-text: #ffffff;
}

body {
  margin: 0;
  font-family: var(--font-family);
  background-color: var(--background-color);
  color: var(--text-color);
  transition: background-color 0.3s, color 0.3s;
}

.app-container {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

.app-header {
  padding: 1rem 2rem;
  background-color: var(--header-bg);
  border-bottom: 1px solid #dee2e6;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.app-main {
  flex-grow: 1;
  padding: 2rem;
}

.app-footer {
  padding: 1rem 2rem;
  background-color: var(--footer-bg);
  border-top: 1px solid #dee2e6;
  text-align: center;
}

button {
  background-color: var(--button-bg);
  color: var(--button-text);
  border: none;
  padding: 0.6em 1.2em;
  border-radius: 8px;
  cursor: pointer;
  font-size: 1em;
  font-weight: 500;
  transition: background-color 0.25s;
}

button:hover {
  opacity: 0.8;
}
```

## Testing Setup

This section includes the necessary configuration and an example test file.

### `src/setupTests.ts`

This file is used to configure or set up the testing framework before each test file in the suite is executed.

```typescript
// jest-dom adds custom jest matchers for asserting on DOM nodes.
// allows you to do things like:
// expect(element).toHaveTextContent(/react/i)
// learn more: https://github.com/testing-library/jest-dom
import '@testing-library/jest-dom';
```

### `src/components/Layout.test.tsx`

An example test for the `Layout` component to verify that it renders correctly and that the theme toggle button works.

```typescript
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { Provider } from 'react-redux';
import { MemoryRouter } from 'react-router-dom';
import { configureStore } from '@reduxjs/toolkit';
import { describe, it, expect, vi } from 'vitest';

import Layout from './Layout';
import themeReducer from '@/features/theme/themeSlice';

// Mock Redux store for testing
const createTestStore = (preloadedState?: any) => {
  return configureStore({
    reducer: {
      theme: themeReducer,
    },
    preloadedState,
  });
};

describe('Layout Component', () => {
  it('renders the header, main content, and footer', () => {
    const store = createTestStore();
    render(
      <Provider store={store}>
        <MemoryRouter>
          <Layout />
        </MemoryRouter>
      </Provider>,
    );

    expect(
      screen.getByRole('heading', { name: /frontend application/i }),
    ).toBeInTheDocument();
    expect(screen.getByRole('main')).toBeInTheDocument();
    expect(screen.getByText(/© \d{4} - Production-Ready App/)).toBeInTheDocument();
  });

  it('toggles the theme when the button is clicked', async () => {
    const store = createTestStore({ theme: { value: 'light' } });
    const user = userEvent.setup();

    render(
      <Provider store={store}>
        <MemoryRouter>
          <Layout />
        </MemoryRouter>
      </Provider>,
    );

    const themeToggleButton = screen.getByRole('button', {
      name: /switch to dark mode/i,
    });
    expect(themeToggleButton).toBeInTheDocument();

    // Click the button
    await user.click(themeToggleButton);

    // Check if the Redux action was dispatched and state changed
    const state = store.getState();
    expect(state.theme.value).toBe('dark');
  });
});
```

## Deployment

This section provides a production-ready Docker setup for containerizing and deploying the frontend application.

### `Dockerfile`

A multi-stage Dockerfile that first builds the application and then serves the static files using a lightweight Nginx server.

```dockerfile
# Stage 1: Build the application
FROM node:20-alpine AS builder

WORKDIR /app

# Copy package.json and package-lock.json
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy the rest of the application source code
COPY . .

# Set build-time environment variables if needed
# ARG VITE_API_BASE_URL
# ENV VITE_API_BASE_URL=$VITE_API_BASE_URL

# Build the project
RUN npm run build

# Stage 2: Serve the application with Nginx
FROM nginx:1.25-alpine

# Copy the built assets from the builder stage
COPY --from=builder /app/dist /usr/share/nginx/html

# Copy the custom Nginx configuration
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Expose port 80
EXPOSE 80

# Start Nginx
CMD ["nginx", "-g", "daemon off;"]
```

### `nginx.conf`

A custom Nginx configuration to correctly serve the single-page application (SPA). It directs all non-file requests to `index.html` to enable client-side routing.

```nginx
server {
    listen 80;
    server_name localhost;

    # Root directory for static files
    root /usr/share/nginx/html;
    index index.html index.htm;

    location / {
        # Try to serve the file directly, otherwise fall back to index.html
        try_files $uri $uri/ /index.html;
    }

    # Optional: Add headers for security
    add_header X-Frame-Options "SAMEORIGIN";
    add_header X-Content-Type-Options "nosniff";
    add_header X-XSS-Protection "1; mode=block";
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;

    # Optional: Gzip compression for better performance
    gzip on;
    gzip_vary on;
    gzip_proxied any;
    gzip_comp_level 6;
    gzip_types text/plain text/css application/json application/javascript text/xml application/xml application/xml+rss text/javascript;
}
```

### `.dockerignore`

This file prevents unnecessary files from being copied into the Docker image, resulting in a smaller and more secure image.

```
# Git
.git
.gitignore

# Node
node_modules

# IDE
.vscode
.idea

# Env
.env
.env.*
!/.env.example

# Logs
npm-debug.log*
yarn-debug.log*
yarn-error.log*

# Build output
dist
dist-ssr
```

### `/.github/workflows/ci.yml`

A sample GitHub Actions workflow for continuous integration. This workflow runs on every push to the `main` branch. It installs dependencies, lints, tests, and builds the application.

```yaml
name: Frontend CI

on:
  push:
    branches: [ "main" ]
  pull_request:
    branches: [ "main" ]

jobs:
  build-and-test:
    runs-on: ubuntu-latest

    strategy:
      matrix:
        node-version: [20.x]

    steps:
    - name: Checkout repository
      uses: actions/checkout@v4

    - name: Use Node.js ${{ matrix.node-version }}
      uses: actions/setup-node@v4
      with:
        node-version: ${{ matrix.node-version }}
        cache: 'npm'

    - name: Install dependencies
      run: npm ci

    - name: Lint code
      run: npm run lint

    - name: Run tests
      run: npm test -- --run # Use --run to exit after tests complete

    - name: Build project
      run: npm run build
      env:
        VITE_API_BASE_URL: ${{ secrets.VITE_API_BASE_URL }} # Example of using secrets for build-time env vars

    # Optional: Step to archive production artifacts
    - name: Archive production artifacts
      uses: actions/upload-artifact@v4
      with:
        name: dist-files
        path: dist
```
✅ Streaming completed.