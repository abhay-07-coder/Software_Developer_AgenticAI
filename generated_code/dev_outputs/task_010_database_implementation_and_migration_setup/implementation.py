As a Senior Full-Stack Software Developer AI Agent, I will now implement the database schema and migration system as requested. I will be using a modern, robust stack consisting of **Node.js, TypeScript, PostgreSQL, and Prisma**. This choice provides strong typing, a powerful ORM with built-in migration capabilities, and a reliable database system, ensuring a production-grade outcome.

The implementation will cover the complete project setup, including dependency management, configuration, schema definition, migration generation, data seeding, and containerization for easy deployment and development.

## Architecture & Design

I've chosen Prisma as the ORM due to its excellent TypeScript support, declarative schema, and integrated migration system. This simplifies database management and ensures type safety between the database and the application logic.

The project structure is organized for clarity and maintainability, separating concerns:

-   `prisma/`: Contains the database schema, migrations, and seeding script.
-   `src/`: Intended for application source code (though this task focuses on the DB layer).
-   `tests/`: Contains tests for the application.
-   `docker-compose.yml`: For setting up a local development environment with PostgreSQL.
-   `Dockerfile`: For containerizing the Node.js application.

The database schema will model a simple blogging platform with Users, Posts, and Categories, demonstrating various relationship types (one-to-one, one-to-many, many-to-many).

## Setup and Deployment Instructions

### Prerequisites

-   Node.js (v18.x or later)
-   npm (v9.x or later)
-   Docker and Docker Compose

### 1. Clone the Project & Install Dependencies

First, set up the project directory and install the required npm packages.

```bash
# Create project directory
mkdir my-app-backend
cd my-app-backend

# Initialize npm project and install dependencies
npm init -y
npm install prisma @prisma/client dotenv bcrypt
npm install -D typescript @types/node @types/bcrypt ts-node jest @types/jest ts-jest
```

### 2. Configure TypeScript

Create a `tsconfig.json` file for the TypeScript compiler.

```bash
# Initialize tsconfig.json
npx tsc --init --rootDir src --outDir dist --lib es2020 --module commonjs --esModuleInterop --strict --skipLibCheck
```
*Note: The command above generates the `tsconfig.json` file provided in the artifacts below.*

### 3. Set Up Environment Variables

Create a `.env` file in the root directory. This file will store the database connection string. **This file should be added to `.gitignore` and never committed to version control.**

```bash
# Create the .env file
touch .env
```

Now, populate `.env` with the content from the artifact below.

### 4. Initialize Prisma

Initialize Prisma in your project. This creates the `prisma` directory and a basic `schema.prisma` file.

```bash
npx prisma init
```

### 5. Start the Database

Use the provided `docker-compose.yml` to start a PostgreSQL instance.

```bash
docker-compose up -d
```

### 6. Run Database Migration

Apply the schema to the database. Prisma will create the migration file and execute it against the database, creating all tables and relationships.

```bash
npx prisma migrate dev --name init
```

This command will:
1.  Read your `prisma/schema.prisma`.
2.  Create a new SQL migration file in `prisma/migrations/`.
3.  Apply the migration to the database.
4.  Generate the Prisma Client (`@prisma/client`) based on your schema.

### 7. Seed the Database

Run the seeding script to populate the database with initial data.

```bash
npx prisma db seed
```

### 8. Running Tests

To verify the database connection and ORM setup, you can run the integration test.

```bash
npx jest
```

## Project Structure

```
.
├── .env
├── .gitignore
├── docker-compose.yml
├── Dockerfile
├── jest.config.js
├── package.json
├── prisma
│   ├── migrations
│   │   └── [timestamp]_init
│   │       └── migration.sql
│   ├── schema.prisma
│   └── seed.ts
├── src
│   └── lib
│       └── prisma.ts
├── tests
│   └── database.integration.test.ts
└── tsconfig.json
```

---

## Code Artifacts

### package.json

This file defines the project's dependencies and scripts for running migrations, seeding, and tests.

```json
{
  "name": "my-app-backend",
  "version": "1.0.0",
  "description": "Database implementation for the project.",
  "main": "dist/index.js",
  "scripts": {
    "build": "tsc",
    "start": "node dist/index.js",
    "dev": "ts-node src/index.ts",
    "test": "jest"
  },
  "prisma": {
    "seed": "ts-node prisma/seed.ts"
  },
  "keywords": [],
  "author": "Senior Full-Stack AI Agent",
  "license": "ISC",
  "dependencies": {
    "@prisma/client": "^5.15.0",
    "bcrypt": "^5.1.1",
    "dotenv": "^16.4.5",
    "prisma": "^5.15.0"
  },
  "devDependencies": {
    "@types/bcrypt": "^5.0.2",
    "@types/jest": "^29.5.12",
    "@types/node": "^20.14.2",
    "jest": "^29.7.0",
    "ts-jest": "^29.1.4",
    "ts-node": "^10.9.2",
    "typescript": "^5.4.5"
  }
}
```

### .env

This file stores sensitive configuration, such as the database URL.

```env
# .env
# Database connection string
# Format: postgresql://[user]:[password]@[host]:[port]/[database]
DATABASE_URL="postgresql://admin:supersecret@localhost:5432/appdb?schema=public"
```

### docker-compose.yml

This file defines the local development environment, including the PostgreSQL database service.

```yaml
version: '3.8'

services:
  postgres:
    image: postgres:15-alpine
    container_name: my_app_postgres
    restart: always
    environment:
      POSTGRES_USER: admin
      POSTGRES_PASSWORD: supersecret
      POSTGRES_DB: appdb
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U admin -d appdb"]
      interval: 10s
      timeout: 5s
      retries: 5

volumes:
  postgres_data:
```

### Dockerfile

A production-ready Dockerfile to containerize the Node.js application.

```dockerfile
# Stage 1: Build the application
FROM node:18-alpine AS builder

WORKDIR /usr/src/app

# Copy package.json and package-lock.json
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy prisma schema
COPY prisma ./prisma/

# Generate Prisma Client
RUN npx prisma generate

# Copy application source code
COPY . .

# Build TypeScript to JavaScript
RUN npm run build

# Stage 2: Production image
FROM node:18-alpine

WORKDIR /usr/src/app

# Copy necessary files from builder stage
COPY --from=builder /usr/src/app/node_modules ./node_modules
COPY --from=builder /usr/src/app/package*.json ./
COPY --from=builder /usr/src/app/dist ./dist
COPY --from=builder /usr/src/app/prisma ./prisma

# Expose the application port
EXPOSE 3000

# Command to run the application
CMD ["node", "dist/index.js"]
```

### .gitignore

Standard gitignore for a Node.js project.

```gitignore
# Dependencies
/node_modules

# Production
/dist

# Logs
logs
*.log
npm-debug.log*
yarn-debug.log*
yarn-error.log*
lerna-debug.log*

# Environment variables
.env
.env.test
.env.production

# IDEs and editors
.idea
.vscode/
*.suo
*.ntvs*
*.njsproj
*.sln
*.sw?

# OS generated files
.DS_Store
Thumbs.db

# Test reports
/coverage
```

### tsconfig.json

TypeScript compiler configuration.

```json
{
  "compilerOptions": {
    "target": "es2020",
    "module": "commonjs",
    "rootDir": "./",
    "outDir": "./dist",
    "esModuleInterop": true,
    "forceConsistentCasingInFileNames": true,
    "strict": true,
    "skipLibCheck": true
  },
  "include": ["src/**/*", "prisma/seed.ts", "tests/**/*"],
  "exclude": ["node_modules"]
}
```

### jest.config.js

Configuration for the Jest testing framework.

```javascript
/** @type {import('ts-jest').JestConfigWithTsJest} */
module.exports = {
  preset: 'ts-jest',
  testEnvironment: 'node',
  testMatch: ['**/tests/**/*.test.ts'],
  verbose: true,
  forceExit: true,
};
```

### prisma/schema.prisma

This is the core of the database implementation. It defines all models, fields, and relations in a declarative way. Prisma uses this file to generate both the SQL migration and the type-safe client.

```prisma
// This is your Prisma schema file,
// learn more about it in the docs: https://pris.ly/d/prisma-schema

// Looking for ways to speed up your queries, or scale easily with your serverless or edge functions?
// Try Prisma Accelerate: https://pris.ly/cli/accelerate-init

generator client {
  provider = "prisma-client-js"
}

datasource db {
  provider = "postgresql"
  url      = env("DATABASE_URL")
}

// Enum for User Roles
enum Role {
  USER
  ADMIN
}

// User model
model User {
  id        String   @id @default(cuid())
  email     String   @unique
  password  String
  name      String?
  role      Role     @default(USER)
  posts     Post[]
  profile   Profile?
  createdAt DateTime @default(now())
  updatedAt DateTime @updatedAt
}

// Profile model (one-to-one with User)
model Profile {
  id     String  @id @default(cuid())
  bio    String?
  user   User    @relation(fields: [userId], references: [id])
  userId String  @unique
}

// Post model
model Post {
  id          String             @id @default(cuid())
  title       String
  content     String?
  published   Boolean            @default(false)
  author      User               @relation(fields: [authorId], references: [id])
  authorId    String
  categories  CategoriesOnPosts[]
  createdAt   DateTime           @default(now())
  updatedAt   DateTime           @updatedAt
}

// Category model
model Category {
  id    String             @id @default(cuid())
  name  String             @unique
  posts CategoriesOnPosts[]
}

// Explicit many-to-many join table for Posts and Categories
model CategoriesOnPosts {
  post       Post     @relation(fields: [postId], references: [id])
  postId     String
  category   Category @relation(fields: [categoryId], references: [id])
  categoryId String
  assignedAt DateTime @default(now())
  assignedBy String // Could be a user's name or ID

  @@id([postId, categoryId])
}
```

### prisma/migrations/[timestamp]_init/migration.sql

This SQL file is **generated by Prisma** (`prisma migrate dev`). It represents the initial migration that creates the database schema.

```sql
-- CreateEnum
CREATE TYPE "Role" AS ENUM ('USER', 'ADMIN');

-- CreateTable
CREATE TABLE "User" (
    "id" TEXT NOT NULL,
    "email" TEXT NOT NULL,
    "password" TEXT NOT NULL,
    "name" TEXT,
    "role" "Role" NOT NULL DEFAULT 'USER',
    "createdAt" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updatedAt" TIMESTAMP(3) NOT NULL,

    CONSTRAINT "User_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "Profile" (
    "id" TEXT NOT NULL,
    "bio" TEXT,
    "userId" TEXT NOT NULL,

    CONSTRAINT "Profile_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "Post" (
    "id" TEXT NOT NULL,
    "title" TEXT NOT NULL,
    "content" TEXT,
    "published" BOOLEAN NOT NULL DEFAULT false,
    "authorId" TEXT NOT NULL,
    "createdAt" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updatedAt" TIMESTAMP(3) NOT NULL,

    CONSTRAINT "Post_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "Category" (
    "id" TEXT NOT NULL,
    "name" TEXT NOT NULL,

    CONSTRAINT "Category_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "CategoriesOnPosts" (
    "postId" TEXT NOT NULL,
    "categoryId" TEXT NOT NULL,
    "assignedAt" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "assignedBy" TEXT NOT NULL,

    CONSTRAINT "CategoriesOnPosts_pkey" PRIMARY KEY ("postId","categoryId")
);

-- CreateIndex
CREATE UNIQUE INDEX "User_email_key" ON "User"("email");

-- CreateIndex
CREATE UNIQUE INDEX "Profile_userId_key" ON "Profile"("userId");

-- CreateIndex
CREATE UNIQUE INDEX "Category_name_key" ON "Category"("name");

-- AddForeignKey
ALTER TABLE "Profile" ADD CONSTRAINT "Profile_userId_fkey" FOREIGN KEY ("userId") REFERENCES "User"("id") ON DELETE RESTRICT ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "Post" ADD CONSTRAINT "Post_authorId_fkey" FOREIGN KEY ("authorId") REFERENCES "User"("id") ON DELETE RESTRICT ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "CategoriesOnPosts" ADD CONSTRAINT "CategoriesOnPosts_postId_fkey" FOREIGN KEY ("postId") REFERENCES "Post"("id") ON DELETE RESTRICT ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "CategoriesOnPosts" ADD CONSTRAINT "CategoriesOnPosts_categoryId_fkey" FOREIGN KEY ("categoryId") REFERENCES "Category"("id") ON DELETE RESTRICT ON UPDATE CASCADE;
```

### prisma/seed.ts

This script populates the database with initial data. It demonstrates creating related records and uses `bcrypt` for secure password hashing.

```typescript
import { PrismaClient } from '@prisma/client';
import * as bcrypt from 'bcrypt';

const prisma = new PrismaClient();

// Function to hash passwords
const hashPassword = (password: string) => {
  const saltRounds = 10;
  return bcrypt.hash(password, saltRounds);
};

async function main() {
  console.log(`Start seeding ...`);

  // Clear existing data
  await prisma.categoriesOnPosts.deleteMany();
  await prisma.category.deleteMany();
  await prisma.post.deleteMany();
  await prisma.profile.deleteMany();
  await prisma.user.deleteMany();
  console.log('Cleared existing data.');

  // Create Users
  const adminPassword = await hashPassword('admin123');
  const userPassword = await hashPassword('user123');

  const adminUser = await prisma.user.create({
    data: {
      email: 'admin@example.com',
      name: 'Alice Admin',
      password: adminPassword,
      role: 'ADMIN',
      profile: {
        create: {
          bio: 'I am the administrator of this platform.',
        },
      },
    },
  });

  const regularUser = await prisma.user.create({
    data: {
      email: 'user@example.com',
      name: 'Bob User',
      password: userPassword,
      role: 'USER',
      profile: {
        create: {
          bio: 'Just a regular user exploring the world.',
        },
      },
    },
  });

  console.log(`Created users: ${adminUser.name}, ${regularUser.name}`);

  // Create Categories
  const techCategory = await prisma.category.create({
    data: { name: 'Technology' },
  });
  const lifestyleCategory = await prisma.category.create({
    data: { name: 'Lifestyle' },
  });
  const travelCategory = await prisma.category.create({
    data: { name: 'Travel' },
  });

  console.log(`Created categories: ${techCategory.name}, ${lifestyleCategory.name}, ${travelCategory.name}`);

  // Create Posts and associate with users and categories
  const post1 = await prisma.post.create({
    data: {
      title: 'Exploring the World of TypeScript',
      content: 'TypeScript offers static typing for JavaScript...',
      published: true,
      authorId: adminUser.id,
      categories: {
        create: [
          {
            assignedBy: adminUser.name!,
            category: {
              connect: { id: techCategory.id },
            },
          },
        ],
      },
    },
  });

  const post2 = await prisma.post.create({
    data: {
      title: 'My Favorite Travel Destinations',
      content: 'From the mountains of Switzerland to the beaches of Bali...',
      published: true,
      authorId: regularUser.id,
      categories: {
        create: [
          {
            assignedBy: regularUser.name!,
            category: {
              connect: { id: travelCategory.id },
            },
          },
          {
            assignedBy: regularUser.name!,
            category: {
              connect: { id: lifestyleCategory.id },
            },
          },
        ],
      },
    },
  });

  console.log(`Created posts: "${post1.title}", "${post2.title}"`);
  console.log(`Seeding finished.`);
}

main()
  .catch((e) => {
    console.error(e);
    process.exit(1);
  })
  .finally(async () => {
    await prisma.$disconnect();
  });
```

### src/lib/prisma.ts

A singleton instance of the Prisma client, which can be imported throughout the application to interact with the database.

```typescript
// src/lib/prisma.ts
import { PrismaClient } from '@prisma/client';

// Add prisma to the NodeJS global type
declare global {
  var prisma: PrismaClient | undefined;
}

// Prevent multiple instances of Prisma Client in development
const prisma = global.prisma || new PrismaClient({
  log: ['query', 'info', 'warn', 'error'],
});

if (process.env.NODE_ENV !== 'production') {
  global.prisma = prisma;
}

export default prisma;
```

### tests/database.integration.test.ts

A simple integration test to verify that the Prisma client can connect to the database and retrieve data seeded by the `seed.ts` script.

```typescript
import prisma from '../src/lib/prisma';

describe('Database Integration', () => {
  afterAll(async () => {
    // Disconnect Prisma client after all tests
    await prisma.$disconnect();
  });

  it('should connect to the database and fetch seeded users', async () => {
    const users = await prisma.user.findMany();
    // The seed script creates 2 users
    expect(users).toHaveLength(2);
    expect(users.map(u => u.email)).toContain('admin@example.com');
    expect(users.map(u => u.email)).toContain('user@example.com');
  });

  it('should fetch a user with their related profile', async () => {
    const adminUser = await prisma.user.findUnique({
      where: { email: 'admin@example.com' },
      include: { profile: true },
    });

    expect(adminUser).not.toBeNull();
    expect(adminUser?.profile).not.toBeNull();
    expect(adminUser?.profile?.bio).toBe('I am the administrator of this platform.');
  });

  it('should fetch a post with its related categories', async () => {
    const techPost = await prisma.post.findFirst({
      where: { title: 'Exploring the World of TypeScript' },
      include: {
        categories: {
          include: {
            category: true,
          },
        },
      },
    });

    expect(techPost).not.toBeNull();
    expect(techPost?.categories).toHaveLength(1);
    expect(techPost?.categories[0].category.name).toBe('Technology');
  });
});
```
✅ Streaming completed.