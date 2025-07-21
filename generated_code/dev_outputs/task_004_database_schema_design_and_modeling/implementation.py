As a Senior Full-Stack Software Developer AI Agent, I will now design and implement the database schema for the e-commerce application. The design prioritizes scalability, performance, and maintainability, providing a solid foundation for the application's data layer.

## Architecture and Design Overview

The database schema is designed for a PostgreSQL backend, a powerful and reliable open-source relational database. The design is normalized to reduce data redundancy and improve data integrity. It is also designed with future microservice separation in mind; for example, `Users`, `Products`, and `Orders` could eventually live in separate services and databases, communicating via their UUIDs.

We will use SQLAlchemy as the ORM (Object-Relational Mapper) and Alembic for database migrations. This combination provides a robust, programmatic way to manage the database schema, which is essential for production environments and CI/CD pipelines.

### Entity-Relationship Diagram (ERD)

Below is a textual representation of the ERD using Mermaid syntax. This diagram illustrates the tables and their relationships.

```mermaid
erDiagram
    users {
        UUID id PK
        varchar email UK
        varchar hashed_password
        varchar full_name
        boolean is_active
        boolean is_superuser
        timestamptz created_at
        timestamptz updated_at
    }

    categories {
        int id PK
        varchar name UK
        varchar slug UK
        text description
        int parent_id FK
        timestamptz created_at
        timestamptz updated_at
    }

    products {
        UUID id PK
        varchar name
        varchar slug UK
        text description
        numeric price
        varchar sku UK
        int stock_quantity
        int category_id FK
        timestamptz created_at
        timestamptz updated_at
    }

    carts {
        UUID id PK
        UUID user_id FK, UK
        timestamptz created_at
        timestamptz updated_at
    }

    cart_items {
        int id PK
        UUID cart_id FK
        UUID product_id FK
        int quantity
        timestamptz added_at
    }

    orders {
        UUID id PK
        UUID user_id FK
        varchar status
        numeric total_amount
        jsonb shipping_address
        jsonb billing_address
        timestamptz created_at
        timestamptz updated_at
    }

    order_items {
        int id PK
        UUID order_id FK
        UUID product_id FK
        int quantity
        numeric price_at_purchase
    }

    users ||--o{ carts : "has one"
    users ||--o{ orders : "places"
    categories ||--o{ products : "contains"
    categories }|--o| categories : "is child of"
    carts ||--|{ cart_items : "contains"
    products ||--o{ cart_items : "is in"
    orders ||--|{ order_items : "contains"
    products ||--o{ order_items : "is in"

```

### Indexing Strategy

Proper indexing is critical for database performance. The following indexing strategy will be implemented:

1.  **Primary Keys**: Automatically indexed by PostgreSQL (`id` columns).
2.  **Unique Constraints**: Automatically indexed to enforce uniqueness (`users.email`, `products.sku`, `products.slug`, `categories.name`, `categories.slug`).
3.  **Foreign Keys**: All foreign key columns (`products.category_id`, `carts.user_id`, `orders.user_id`, etc.) will be indexed to optimize `JOIN` performance.
4.  **Frequently Queried Columns**:
    *   `products.name`: To accelerate text-based searches and sorting. A B-tree index is suitable for this. For more advanced full-text search, a `GIN` or `GiST` index would be a better choice.
    *   `orders.status`: To quickly filter orders by their status (e.g., finding all "pending" orders).
    *   `categories.parent_id`: To efficiently query for subcategories.

---

## Setup and Configuration

### 1. Dependencies

Create a `requirements.txt` file with the necessary Python packages.

```text
# requirements.txt
# Core dependencies for data layer
sqlalchemy[psycopg2-binary]==2.0.23
alembic==1.13.0
python-dotenv==1.0.0
pydantic==2.5.2
greenlet==3.0.1
```

### 2. Environment Configuration

Create a `.env` file in the project root to store the database connection string. **Never commit this file to version control.**

```ini
# .env
# Example for a local PostgreSQL instance
DATABASE_URL="postgresql+psycopg2://user:password@localhost:5432/ecommerce_db"
```

### 3. Configuration Loading

Create a `config.py` file to load the environment variables.

```python
# config.py
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Settings:
    """Application configuration settings."""
    DATABASE_URL: str = os.getenv("DATABASE_URL")

settings = Settings()

```

---

## Database Schema Definition (SQL DDL)

This file contains the raw SQL `CREATE TABLE` statements. It serves as a reference and can be used to set up the database manually if needed.

```sql
-- database/DDL.sql

-- For UUID generation
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Enum type for order status for better data integrity
CREATE TYPE order_status_enum AS ENUM ('pending', 'processing', 'shipped', 'delivered', 'cancelled');

-- Users Table
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    email VARCHAR(255) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    full_name VARCHAR(100),
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    is_superuser BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Categories Table with self-referencing key for hierarchy
CREATE TABLE categories (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL,
    slug VARCHAR(120) UNIQUE NOT NULL,
    description TEXT,
    parent_id INTEGER REFERENCES categories(id) ON DELETE SET NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Products Table
CREATE TABLE products (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(255) NOT NULL,
    slug VARCHAR(255) UNIQUE NOT NULL,
    description TEXT,
    price NUMERIC(10, 2) NOT NULL CHECK (price >= 0),
    sku VARCHAR(100) UNIQUE NOT NULL,
    stock_quantity INTEGER NOT NULL DEFAULT 0 CHECK (stock_quantity >= 0),
    category_id INTEGER REFERENCES categories(id) ON DELETE SET NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Carts Table (One-to-one with Users)
CREATE TABLE carts (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID UNIQUE NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Cart Items Table (Join table for Carts and Products)
CREATE TABLE cart_items (
    id SERIAL PRIMARY KEY,
    cart_id UUID NOT NULL REFERENCES carts(id) ON DELETE CASCADE,
    product_id UUID NOT NULL REFERENCES products(id) ON DELETE CASCADE,
    quantity INTEGER NOT NULL CHECK (quantity > 0),
    added_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE (cart_id, product_id)
);

-- Orders Table
CREATE TABLE orders (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE SET NULL,
    status order_status_enum NOT NULL DEFAULT 'pending',
    total_amount NUMERIC(10, 2) NOT NULL CHECK (total_amount >= 0),
    shipping_address JSONB,
    billing_address JSONB,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Order Items Table (Join table for Orders and Products)
CREATE TABLE order_items (
    id SERIAL PRIMARY KEY,
    order_id UUID NOT NULL REFERENCES orders(id) ON DELETE CASCADE,
    product_id UUID NOT NULL REFERENCES products(id) ON DELETE RESTRICT,
    quantity INTEGER NOT NULL CHECK (quantity > 0),
    price_at_purchase NUMERIC(10, 2) NOT NULL CHECK (price_at_purchase >= 0)
);

-- Indexes for performance
CREATE INDEX idx_categories_parent_id ON categories(parent_id);
CREATE INDEX idx_products_name ON products(name);
CREATE INDEX idx_products_category_id ON products(category_id);
CREATE INDEX idx_orders_user_id ON orders(user_id);
CREATE INDEX idx_orders_status ON orders(status);
CREATE INDEX idx_cart_items_cart_id ON cart_items(cart_id);
CREATE INDEX idx_cart_items_product_id ON cart_items(product_id);
CREATE INDEX idx_order_items_order_id ON order_items(order_id);
CREATE INDEX idx_order_items_product_id ON order_items(product_id);

-- Trigger to update 'updated_at' timestamps
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
   NEW.updated_at = NOW();
   RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_users_updated_at BEFORE UPDATE ON users FOR EACH ROW EXECUTE PROCEDURE update_updated_at_column();
CREATE TRIGGER update_categories_updated_at BEFORE UPDATE ON categories FOR EACH ROW EXECUTE PROCEDURE update_updated_at_column();
CREATE TRIGGER update_products_updated_at BEFORE UPDATE ON products FOR EACH ROW EXECUTE PROCEDURE update_updated_at_column();
CREATE TRIGGER update_carts_updated_at BEFORE UPDATE ON carts FOR EACH ROW EXECUTE PROCEDURE update_updated_at_column();
CREATE TRIGGER update_orders_updated_at BEFORE UPDATE ON orders FOR EACH ROW EXECUTE PROCEDURE update_updated_at_column();
```

---

## ORM Models (SQLAlchemy)

These Python classes map directly to the database tables, providing a high-level, object-oriented interface for all database operations.

### `database/models/base.py`
```python
# database/models/base.py
from sqlalchemy import MetaData
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.sql import func
from datetime import datetime
import uuid

# Define naming conventions for constraints to ensure Alembic generates predictable migration scripts.
convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}

metadata = MetaData(naming_convention=convention)

class Base(DeclarativeBase):
    """Base class for all ORM models."""
    metadata = metadata

class TimestampMixin:
    """Mixin to add created_at and updated_at timestamp columns to models."""
    created_at: Mapped[datetime] = mapped_column(
        server_default=func.now(),
        nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )

def gen_uuid():
    return uuid.uuid4()
```

### `database/models/user.py`
```python
# database/models/user.py
from sqlalchemy import String, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
import uuid

from .base import Base, TimestampMixin, gen_uuid

class User(Base, TimestampMixin):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=gen_uuid
    )
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    full_name: Mapped[str | None] = mapped_column(String(100))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    is_superuser: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    cart: Mapped["Cart"] = relationship(back_populates="user", cascade="all, delete-orphan")
    orders: Mapped[list["Order"]] = relationship(back_populates="user")

    def __repr__(self):
        return f"<User(id={self.id}, email='{self.email}')>"
```

### `database/models/category.py`
```python
# database/models/category.py
from sqlalchemy import String, Text, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional

from .base import Base, TimestampMixin

class Category(Base, TimestampMixin):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    slug: Mapped[str] = mapped_column(String(120), unique=True, nullable=False, index=True)
    description: Mapped[str | None] = mapped_column(Text)
    
    parent_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("categories.id"), index=True)
    parent: Mapped[Optional["Category"]] = relationship(back_populates="children", remote_side=[id])
    children: Mapped[list["Category"]] = relationship(back_populates="parent", cascade="all, delete-orphan")
    
    products: Mapped[list["Product"]] = relationship(back_populates="category")

    def __repr__(self):
        return f"<Category(id={self.id}, name='{self.name}')>"
```

### `database/models/product.py`
```python
# database/models/product.py
from sqlalchemy import String, Text, Numeric, Integer, ForeignKey, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
import uuid

from .base import Base, TimestampMixin, gen_uuid

class Product(Base, TimestampMixin):
    __tablename__ = "products"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=gen_uuid
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    slug: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    description: Mapped[str | None] = mapped_column(Text)
    price: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    sku: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    stock_quantity: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    
    category_id: Mapped[int | None] = mapped_column(Integer, ForeignKey("categories.id"), index=True)
    category: Mapped["Category"] = relationship(back_populates="products")

    __table_args__ = (
        CheckConstraint('price >= 0', name='ck_products_price_non_negative'),
        CheckConstraint('stock_quantity >= 0', name='ck_products_stock_non_negative'),
    )

    def __repr__(self):
        return f"<Product(id={self.id}, name='{self.name}', price={self.price})>"
```

### `database/models/cart.py`
```python
# database/models/cart.py
from sqlalchemy import ForeignKey, Integer, UniqueConstraint, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
import uuid

from .base import Base, TimestampMixin, gen_uuid

class Cart(Base, TimestampMixin):
    __tablename__ = "carts"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=gen_uuid
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False
    )

    user: Mapped["User"] = relationship(back_populates="cart")
    items: Mapped[list["CartItem"]] = relationship(back_populates="cart", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Cart(id={self.id}, user_id={self.user_id})>"

class CartItem(Base):
    __tablename__ = "cart_items"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    cart_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("carts.id", ondelete="CASCADE"), nullable=False
    )
    product_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("products.id", ondelete="CASCADE"), nullable=False
    )
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    added_at: Mapped[datetime] = mapped_column(server_default=func.now(), nullable=False)

    cart: Mapped["Cart"] = relationship(back_populates="items")
    product: Mapped["Product"] = relationship()

    __table_args__ = (
        UniqueConstraint('cart_id', 'product_id', name='uq_cart_items_cart_product'),
        CheckConstraint('quantity > 0', name='ck_cart_items_quantity_positive'),
    )

    def __repr__(self):
        return f"<CartItem(id={self.id}, product_id={self.product_id}, quantity={self.quantity})>"
```

### `database/models/order.py`
```python
# database/models/order.py
from sqlalchemy import ForeignKey, Integer, Numeric, String, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID, JSONB, ENUM
import uuid
from enum import Enum

from .base import Base, TimestampMixin, gen_uuid

class OrderStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"

order_status_enum = ENUM(OrderStatus, name="order_status_enum", create_type=False)

class Order(Base, TimestampMixin):
    __tablename__ = "orders"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=gen_uuid
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True
    )
    status: Mapped[OrderStatus] = mapped_column(
        order_status_enum, nullable=False, default=OrderStatus.PENDING, index=True
    )
    total_amount: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    shipping_address: Mapped[dict | None] = mapped_column(JSONB)
    billing_address: Mapped[dict | None] = mapped_column(JSONB)

    user: Mapped["User"] = relationship(back_populates="orders")
    items: Mapped[list["OrderItem"]] = relationship(back_populates="order", cascade="all, delete-orphan")

    __table_args__ = (
        CheckConstraint('total_amount >= 0', name='ck_orders_total_amount_non_negative'),
    )

    def __repr__(self):
        return f"<Order(id={self.id}, status='{self.status}', total={self.total_amount})>"

class OrderItem(Base):
    __tablename__ = "order_items"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    order_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("orders.id", ondelete="CASCADE"), nullable=False
    )
    product_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("products.id", ondelete="RESTRICT"), nullable=False
    )
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    price_at_purchase: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)

    order: Mapped["Order"] = relationship(back_populates="items")
    product: Mapped["Product"] = relationship()

    __table_args__ = (
        CheckConstraint('quantity > 0', name='ck_order_items_quantity_positive'),
        CheckConstraint('price_at_purchase >= 0', name='ck_order_items_price_non_negative'),
    )

    def __repr__(self):
        return f"<OrderItem(id={self.id}, product_id={self.product_id}, quantity={self.quantity})>"
```

### `database/models/__init__.py`
```python
# database/models/__init__.py
# This file makes the 'models' directory a Python package and is a good place
# to import all models so they are registered with SQLAlchemy's Base.

from .base import Base
from .user import User
from .category import Category
from .product import Product
from .cart import Cart, CartItem
from .order import Order, OrderItem

__all__ = [
    "Base",
    "User",
    "Category",
    "Product",
    "Cart",
    "CartItem",
    "Order",
    "OrderItem",
]
```

---

## Database Migrations (Alembic)

Alembic is the standard tool for managing SQLAlchemy database migrations.

### 1. Initialize Alembic

Run this command in your terminal at the project root:

```bash
alembic init alembic
```

This creates the `alembic` directory and `alembic.ini` file.

### 2. Configure Alembic

Modify `alembic.ini` and `alembic/env.py`.

#### `alembic.ini`
Update the `sqlalchemy.url` line to use the configuration from our `.env` file.

```ini
# alembic.ini
[alembic]
# ... (rest of the file) ...

# path to migration scripts
script_location = alembic

# ... (rest of the file) ...

# Logging configuration
# ... (rest of the file) ...

# Add this section to read from config.py
[post_write_hooks]
hooks = autopep8
autopep8.type = exec
autopep8.entrypoint = autopep8
autopep8.options = --in-place --aggressive --aggressive %(path)s

# Set the sqlalchemy.url from our config file
# The actual value will be loaded in env.py
sqlalchemy.url = driver://user:pass@localhost/dbname
```

#### `alembic/env.py`
Modify this file to point to your models and use the database URL from `config.py`.

```python
# alembic/env.py
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

# --- START of modifications ---

# Import your models' Base
from database.models import Base
# Import your settings
from config import settings

# Set the target metadata for autogeneration
target_metadata = Base.metadata

# Set the database URL from your settings
# This overrides the value in alembic.ini
config.set_main_option('sqlalchemy.url', settings.DATABASE_URL)

# --- END of modifications ---

def run_migrations_offline() -> None:
    # ... (rest of the function) ...

def run_migrations_online() -> None:
    """Run migrations in 'online' mode.
    # ... (rest of the function) ...
    """
    connectable = engine_from_config(
        config.get_section(config.config_main_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, 
            target_metadata=target_metadata,
            # Add this line to handle PostgreSQL types like ENUM
            render_as_batch=True
        )

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
```

### 3. Generate Initial Migration

Now, generate the first migration script based on the ORM models.

```bash
alembic revision --autogenerate -m "Initial schema setup"
```

This will create a new file in `alembic/versions/`, for example `alembic/versions/xxxxxxxx_initial_schema_setup.py`. The contents will be the Python code required to create all the tables, indexes, and constraints defined in your models.

### 4. Apply the Migration

To apply the migration and create the tables in your database, run:

```bash
alembic upgrade head
```

Your database now matches the schema defined in your SQLAlchemy models.

---

## Seed Data

This SQL script can be used to populate the database with some initial data for testing and development.

```sql
-- database/seed_data.sql

-- Note: UUIDs are hardcoded for predictability in a development environment.
-- In a real scenario, these would be generated.

-- Create Users
INSERT INTO users (id, email, hashed_password, full_name, is_active, is_superuser) VALUES
('a1b2c3d4-e5f6-7890-1234-567890abcdef', 'alice@example.com', '$2b$12$DbmI/y13xImx2rg2kQYwY.2Y2dJ.J.s2s3s4s5s6s7s8s9s0', 'Alice Smith', TRUE, FALSE),
('b2c3d4e5-f6a7-8901-2345-67890abcdef0', 'bob@example.com', '$2b$12$EfgH/y13xImx2rg2kQYwY.2Y2dJ.J.s2s3s4s5s6s7s8s9s0', 'Bob Johnson', TRUE, FALSE),
('c3d4e5f6-a7b8-9012-3456-7890abcdef1', 'admin@example.com', '$2b$12$FghI/y13xImx2rg2kQYwY.2Y2dJ.J.s2s3s4s5s6s7s8s9s0', 'Admin User', TRUE, TRUE);

-- Create Categories
INSERT INTO categories (id, name, slug, description, parent_id) VALUES
(1, 'Electronics', 'electronics', 'Gadgets and devices', NULL),
(2, 'Books', 'books', 'Paper and digital books', NULL),
(3, 'Laptops', 'laptops', 'Portable computers', 1),
(4, 'Smartphones', 'smartphones', 'Mobile phones', 1),
(5, 'Science Fiction', 'science-fiction', 'Books about the future', 2);

-- Manually update sequence for categories PK after explicit insertion
SELECT setval('categories_id_seq', (SELECT MAX(id) FROM categories));

-- Create Products
INSERT INTO products (id, name, slug, description, price, sku, stock_quantity, category_id) VALUES
('d4e5f6a7-b8c9-0123-4567-890abcdef12', 'Pro Laptop 15"', 'pro-laptop-15', 'A powerful laptop for professionals.', 1999.99, 'PROLAP15-2023', 50, 3),
('e5f6a7b8-c9d0-1234-5678-90abcdef234', 'SmartPhone X', 'smartphone-x', 'The latest smartphone with AI features.', 899.50, 'SMARTX-2023', 150, 4),
('f6a7b8c9-d0e1-2345-6789-0abcdef345', 'Dune', 'dune-book', 'Classic science fiction novel by Frank Herbert.', 15.75, 'BOOK-DUNE-PB', 200, 5);

-- Create Carts for Users
INSERT INTO carts (id, user_id) VALUES
('a1b2c3d4-e5f6-7890-1234-567890cart01', 'a1b2c3d4-e5f6-7890-1234-567890abcdef'),
('b2c3d4e5-f6a7-8901-2345-67890cart02', 'b2c3d4e5-f6a7-8901-2345-67890abcdef0');

-- Add items to Alice's cart
INSERT INTO cart_items (cart_id, product_id, quantity) VALUES
('a1b2c3d4-e5f6-7890-1234-567890cart01', 'd4e5f6a7-b8c9-0123-4567-890abcdef12', 1),
('a1b2c3d4-e5f6-7890-1234-567890cart01', 'f6a7b8c9-d0e1-2345-6789-0abcdef345', 2);

-- Create a past order for Bob
INSERT INTO orders (id, user_id, status, total_amount, shipping_address) VALUES
('c3d4e5f6-a7b8-9012-3456-7890order01', 'b2c3d4e5-f6a7-8901-2345-67890abcdef0', 'delivered', 930.00, '{"street": "123 Main St", "city": "Anytown", "zip": "12345"}');

-- Add items to Bob's past order
INSERT INTO order_items (order_id, product_id, quantity, price_at_purchase) VALUES
('c3d4e5f6-a7b8-9012-3456-7890order01', 'e5f6a7b8-c9d0-1234-5678-90abcdef234', 1, 899.50),
('c3d4e5f6-a7b8-9012-3456-7890order01', 'f6a7b8c9-d0e1-2345-6789-0abcdef345', 2, 15.25); -- Price was slightly different at time of purchase

```
✅ Streaming completed.