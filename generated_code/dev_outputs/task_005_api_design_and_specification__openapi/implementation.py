As a Senior Full-Stack Software Developer AI Agent, I will now design and create the OpenAPI 3.0 specification for the e-commerce platform. This specification will serve as the single source of truth for the API, detailing all resources, endpoints, data models, and authentication mechanisms.

The design adheres to RESTful principles, is structured for clarity and reusability, and includes considerations for security, pagination, and comprehensive error handling, making it suitable for a production-grade microservices environment.

## Architecture and Design Decisions

The API is designed with a resource-oriented approach. Endpoints are grouped logically by resources: `Auth`, `Users`, `Products`, `Cart`, and `Orders`. This structure is intuitive for frontend developers and facilitates clean backend service separation.

### Key Design Choices:

*   **Stateless Authentication**: We will use JSON Web Tokens (JWT) for authentication. The client receives a token upon login and includes it in the `Authorization` header for all protected requests. This is a standard, scalable approach for modern APIs.
*   **Standardized Error Responses**: A consistent error response schema (`ErrorResponse`) is used across the API. This simplifies error handling on the client side.
*   **Pagination**: All list endpoints that can return a large number of items (e.g., `GET /products`, `GET /orders`) implement cursor-based or offset-based pagination to ensure performance and prevent overloading the client or server.
*   **Role-Based Access Control (RBAC)**: While OpenAPI 3.0 doesn't have a first-class field for roles, the documentation for each endpoint clearly specifies the required access level (e.g., "Admin only"). This is a critical piece of information for both frontend and backend developers.
*   **Component-Based & DRY Specification**: The specification makes extensive use of components (`schemas`, `responses`, `securitySchemes`) to promote reusability and maintainability. This avoids duplicating definitions and ensures consistency.

### How to Use This Specification

This `openapi.yaml` file can be used with various tools:

1.  **Swagger UI / Redoc**: To generate interactive API documentation that developers can browse and test.
2.  **Swagger Editor**: To visualize and edit the API design.
3.  **Code Generators**: To automatically generate client SDKs (e.g., for TypeScript, Java, Python) and server-side boilerplate code, ensuring that the implementation stays in sync with the design.

---

## E-commerce API - OpenAPI Specification

Below is the complete `openapi.yaml` file. This file defines the entire API surface for the e-commerce platform.

```yaml
# -----------------------------------------------------------------------------
# E-commerce Platform API Specification
# Version: 1.0.0
#
# This document defines the RESTful API for the E-commerce platform,
# covering user management, product catalog, shopping cart, and order processing.
#
# It adheres to the OpenAPI 3.0.3 specification.
# -----------------------------------------------------------------------------

openapi: 3.0.3
info:
  title: "E-commerce Platform API"
  description: |
    A comprehensive API for managing users, products, shopping carts, and orders for an online store.
    The API uses JWT for authentication and provides standard RESTful endpoints for all resources.
  version: "1.0.0"
  contact:
    name: "E-commerce Platform Dev Team"
    email: "dev@example-commerce.com"
  license:
    name: "MIT"
    url: "https://opensource.org/licenses/MIT"

servers:
  - url: "https://api.example-commerce.com/v1"
    description: "Production Server"
  - url: "https://api.staging.example-commerce.com/v1"
    description: "Staging Server"
  - url: "http://localhost:8000/v1"
    description: "Local Development Server"

tags:
  - name: "Auth"
    description: "User authentication and session management."
  - name: "Users"
    description: "User profile management."
  - name: "Products"
    description: "Product catalog management."
  - name: "Cart"
    description: "User's shopping cart operations."
  - name: "Orders"
    description: "Order creation and history."

# -----------------------------------------------------------------------------
#  Paths - API Endpoints
# -----------------------------------------------------------------------------

paths:
  # --- Auth Endpoints ---
  /auth/register:
    post:
      tags:
        - "Auth"
      summary: "Register a new user"
      description: "Creates a new user account. Returns the created user's details without the password."
      operationId: "registerUser"
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: "#/components/schemas/UserCreate"
      responses:
        "201":
          description: "User created successfully."
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/User"
        "400":
          $ref: "#/components/responses/BadRequestError"
        "409":
          description: "Conflict - A user with the given email or username already exists."
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/ErrorResponse"

  /auth/login:
    post:
      tags:
        - "Auth"
      summary: "Log in a user"
      description: "Authenticates a user with email and password, returning a JWT access token."
      operationId: "loginUser"
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: "#/components/schemas/UserLogin"
      responses:
        "200":
          description: "Login successful."
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/AuthToken"
        "400":
          $ref: "#/components/responses/BadRequestError"
        "401":
          $ref: "#/components/responses/UnauthorizedError"

  # --- User Endpoints ---
  /users/me:
    get:
      tags:
        - "Users"
      summary: "Get current user's profile"
      description: "Retrieves the profile information for the currently authenticated user."
      operationId: "getCurrentUser"
      security:
        - bearerAuth: []
      responses:
        "200":
          description: "Successful retrieval of user profile."
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/User"
        "401":
          $ref: "#/components/responses/UnauthorizedError"
    put:
      tags:
        - "Users"
      summary: "Update current user's profile"
      description: "Updates the profile information for the currently authenticated user."
      operationId: "updateCurrentUser"
      security:
        - bearerAuth: []
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: "#/components/schemas/UserUpdate"
      responses:
        "200":
          description: "User profile updated successfully."
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/User"
        "400":
          $ref: "#/components/responses/BadRequestError"
        "401":
          $ref: "#/components/responses/UnauthorizedError"

  # --- Product Endpoints ---
  /products:
    get:
      tags:
        - "Products"
      summary: "List all products"
      description: "Retrieves a paginated list of all available products. This endpoint is public."
      operationId: "listProducts"
      parameters:
        - $ref: "#/components/parameters/PageQuery"
        - $ref: "#/components/parameters/PageSizeQuery"
        - name: "category"
          in: "query"
          description: "Filter products by category name."
          schema:
            type: "string"
        - name: "sortBy"
          in: "query"
          description: "Sort products by a specific field (e.g., 'price', 'name')."
          schema:
            type: "string"
            enum: ["price", "name", "created_at"]
        - name: "sortOrder"
          in: "query"
          description: "Sort order ('asc' or 'desc')."
          schema:
            type: "string"
            enum: ["asc", "desc"]
            default: "asc"
      responses:
        "200":
          description: "A paginated list of products."
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/PaginatedProducts"
    post:
      tags:
        - "Products"
      summary: "Create a new product"
      description: "Adds a new product to the catalog. Requires admin privileges."
      operationId: "createProduct"
      security:
        - bearerAuth: []
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: "#/components/schemas/ProductCreate"
      responses:
        "201":
          description: "Product created successfully."
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/Product"
        "400":
          $ref: "#/components/responses/BadRequestError"
        "401":
          $ref: "#/components/responses/UnauthorizedError"
        "403":
          $ref: "#/components/responses/ForbiddenError"

  /products/{productId}:
    get:
      tags:
        - "Products"
      summary: "Get product by ID"
      description: "Retrieves details for a single product by its ID. This endpoint is public."
      operationId: "getProductById"
      parameters:
        - $ref: "#/components/parameters/ProductIdPath"
      responses:
        "200":
          description: "Product details."
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/Product"
        "404":
          $ref: "#/components/responses/NotFoundError"
    put:
      tags:
        - "Products"
      summary: "Update a product"
      description: "Updates an existing product's details. Requires admin privileges."
      operationId: "updateProduct"
      security:
        - bearerAuth: []
      parameters:
        - $ref: "#/components/parameters/ProductIdPath"
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: "#/components/schemas/ProductUpdate"
      responses:
        "200":
          description: "Product updated successfully."
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/Product"
        "400":
          $ref: "#/components/responses/BadRequestError"
        "401":
          $ref: "#/components/responses/UnauthorizedError"
        "403":
          $ref: "#/components/responses/ForbiddenError"
        "404":
          $ref: "#/components/responses/NotFoundError"
    delete:
      tags:
        - "Products"
      summary: "Delete a product"
      description: "Deletes a product from the catalog. Requires admin privileges."
      operationId: "deleteProduct"
      security:
        - bearerAuth: []
      parameters:
        - $ref: "#/components/parameters/ProductIdPath"
      responses:
        "204":
          description: "Product deleted successfully."
        "401":
          $ref: "#/components/responses/UnauthorizedError"
        "403":
          $ref: "#/components/responses/ForbiddenError"
        "404":
          $ref: "#/components/responses/NotFoundError"

  # --- Cart Endpoints ---
  /cart:
    get:
      tags:
        - "Cart"
      summary: "Get the user's cart"
      description: "Retrieves the contents of the current user's shopping cart."
      operationId: "getCart"
      security:
        - bearerAuth: []
      responses:
        "200":
          description: "The user's shopping cart."
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/Cart"
        "401":
          $ref: "#/components/responses/UnauthorizedError"
    delete:
      tags:
        - "Cart"
      summary: "Clear the user's cart"
      description: "Removes all items from the current user's shopping cart."
      operationId: "clearCart"
      security:
        - bearerAuth: []
      responses:
        "204":
          description: "Cart cleared successfully."
        "401":
          $ref: "#/components/responses/UnauthorizedError"

  /cart/items:
    post:
      tags:
        - "Cart"
      summary: "Add an item to the cart"
      description: "Adds a product to the current user's shopping cart. If the item already exists, its quantity is updated."
      operationId: "addCartItem"
      security:
        - bearerAuth: []
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: "#/components/schemas/CartItemAdd"
      responses:
        "200":
          description: "Item added/updated successfully. Returns the updated cart."
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/Cart"
        "400":
          $ref: "#/components/responses/BadRequestError"
        "401":
          $ref: "#/components/responses/UnauthorizedError"
        "404":
          description: "Product not found."
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/ErrorResponse"

  /cart/items/{productId}:
    put:
      tags:
        - "Cart"
      summary: "Update item quantity in cart"
      description: "Updates the quantity of a specific product in the user's cart."
      operationId: "updateCartItem"
      security:
        - bearerAuth: []
      parameters:
        - $ref: "#/components/parameters/ProductIdPath"
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: "#/components/schemas/CartItemUpdate"
      responses:
        "200":
          description: "Item quantity updated. Returns the updated cart."
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/Cart"
        "400":
          $ref: "#/components/responses/BadRequestError"
        "401":
          $ref: "#/components/responses/UnauthorizedError"
        "404":
          description: "Product not found in cart."
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/ErrorResponse"
    delete:
      tags:
        - "Cart"
      summary: "Remove an item from the cart"
      description: "Removes a specific product from the user's shopping cart."
      operationId: "removeCartItem"
      security:
        - bearerAuth: []
      parameters:
        - $ref: "#/components/parameters/ProductIdPath"
      responses:
        "200":
          description: "Item removed successfully. Returns the updated cart."
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/Cart"
        "401":
          $ref: "#/components/responses/UnauthorizedError"
        "404":
          description: "Product not found in cart."
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/ErrorResponse"

  # --- Order Endpoints ---
  /orders:
    post:
      tags:
        - "Orders"
      summary: "Create an order"
      description: "Creates a new order from the items in the user's current cart. The cart will be cleared after the order is successfully created."
      operationId: "createOrder"
      security:
        - bearerAuth: []
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: "#/components/schemas/OrderCreate"
      responses:
        "201":
          description: "Order created successfully."
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/Order"
        "400":
          description: "Bad Request (e.g., cart is empty, item out of stock)."
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/ErrorResponse"
        "401":
          $ref: "#/components/responses/UnauthorizedError"
    get:
      tags:
        - "Orders"
      summary: "List user's orders"
      description: "Retrieves a paginated list of the current user's past orders."
      operationId: "listUserOrders"
      security:
        - bearerAuth: []
      parameters:
        - $ref: "#/components/parameters/PageQuery"
        - $ref: "#/components/parameters/PageSizeQuery"
      responses:
        "200":
          description: "A paginated list of orders."
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/PaginatedOrders"
        "401":
          $ref: "#/components/responses/UnauthorizedError"

  /orders/{orderId}:
    get:
      tags:
        - "Orders"
      summary: "Get order by ID"
      description: "Retrieves details for a specific order. Users can only access their own orders. Admins can access any order."
      operationId: "getOrderById"
      security:
        - bearerAuth: []
      parameters:
        - $ref: "#/components/parameters/OrderIdPath"
      responses:
        "200":
          description: "Order details."
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/Order"
        "401":
          $ref: "#/components/responses/UnauthorizedError"
        "403":
          $ref: "#/components/responses/ForbiddenError"
        "404":
          $ref: "#/components/responses/NotFoundError"

# -----------------------------------------------------------------------------
#  Components - Reusable definitions
# -----------------------------------------------------------------------------

components:
  # --- Security Schemes ---
  securitySchemes:
    bearerAuth:
      type: "http"
      scheme: "bearer"
      bearerFormat: "JWT"
      description: "JWT-based authentication. The token should be provided in the Authorization header as 'Bearer <token>'."

  # --- Parameters ---
  parameters:
    ProductIdPath:
      name: "productId"
      in: "path"
      required: true
      description: "The unique identifier of the product."
      schema:
        type: "string"
        format: "uuid"
    OrderIdPath:
      name: "orderId"
      in: "path"
      required: true
      description: "The unique identifier of the order."
      schema:
        type: "string"
        format: "uuid"
    PageQuery:
      name: "page"
      in: "query"
      description: "The page number to retrieve."
      schema:
        type: "integer"
        minimum: 1
        default: 1
    PageSizeQuery:
      name: "pageSize"
      in: "query"
      description: "The number of items to retrieve per page."
      schema:
        type: "integer"
        minimum: 1
        maximum: 100
        default: 20

  # --- Responses ---
  responses:
    BadRequestError:
      description: "Bad Request - The request was malformed or contained invalid parameters."
      content:
        application/json:
          schema:
            $ref: "#/components/schemas/ErrorResponse"
    UnauthorizedError:
      description: "Unauthorized - Authentication credentials were missing or invalid."
      content:
        application/json:
          schema:
            $ref: "#/components/schemas/ErrorResponse"
    ForbiddenError:
      description: "Forbidden - The authenticated user does not have permission to perform this action."
      content:
        application/json:
          schema:
            $ref: "#/components/schemas/ErrorResponse"
    NotFoundError:
      description: "Not Found - The requested resource could not be found."
      content:
        application/json:
          schema:
            $ref: "#/components/schemas/ErrorResponse"

  # --- Schemas (Data Models) ---
  schemas:
    # --- Base Models ---
    ErrorResponse:
      type: "object"
      properties:
        statusCode:
          type: "integer"
          example: 400
        error:
          type: "string"
          example: "Bad Request"
        message:
          type: "string"
          example: "Invalid input for field 'email'."
    PaginationInfo:
      type: "object"
      properties:
        totalItems:
          type: "integer"
          example: 150
        totalPages:
          type: "integer"
          example: 8
        currentPage:
          type: "integer"
          example: 1
        pageSize:
          type: "integer"
          example: 20

    # --- Auth Schemas ---
    UserLogin:
      type: "object"
      required:
        - "email"
        - "password"
      properties:
        email:
          type: "string"
          format: "email"
          example: "john.doe@example.com"
        password:
          type: "string"
          format: "password"
          example: "Str0ngP@ssw0rd!"
    AuthToken:
      type: "object"
      properties:
        accessToken:
          type: "string"
          example: "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
        tokenType:
          type: "string"
          example: "bearer"

    # --- User Schemas ---
    User:
      type: "object"
      properties:
        id:
          type: "string"
          format: "uuid"
          readOnly: true
          example: "d290f1ee-6c54-4b01-90e6-d701748f0851"
        username:
          type: "string"
          example: "johndoe"
        email:
          type: "string"
          format: "email"
          example: "john.doe@example.com"
        role:
          type: "string"
          enum: ["user", "admin"]
          example: "user"
        createdAt:
          type: "string"
          format: "date-time"
          readOnly: true
        updatedAt:
          type: "string"
          format: "date-time"
          readOnly: true
    UserCreate:
      type: "object"
      required:
        - "username"
        - "email"
        - "password"
      properties:
        username:
          type: "string"
          minLength: 3
          maxLength: 30
          example: "johndoe"
        email:
          type: "string"
          format: "email"
          example: "john.doe@example.com"
        password:
          type: "string"
          format: "password"
          minLength: 8
          example: "Str0ngP@ssw0rd!"
    UserUpdate:
      type: "object"
      properties:
        email:
          type: "string"
          format: "email"
          example: "john.d.doe@example.com"
        username:
          type: "string"
          minLength: 3
          maxLength: 30
          example: "john_doe_1"

    # --- Product Schemas ---
    Product:
      type: "object"
      properties:
        id:
          type: "string"
          format: "uuid"
          readOnly: true
          example: "c7a1e3f4-5b6d-4c7a-8e9f-0a1b2c3d4e5f"
        name:
          type: "string"
          example: "Wireless Mouse"
        description:
          type: "string"
          example: "A high-precision wireless optical mouse."
        price:
          type: "number"
          format: "float"
          example: 25.99
        sku:
          type: "string"
          example: "WM-102-BLK"
        stockQuantity:
          type: "integer"
          example: 150
        createdAt:
          type: "string"
          format: "date-time"
          readOnly: true
        updatedAt:
          type: "string"
          format: "date-time"
          readOnly: true
    ProductCreate:
      type: "object"
      required:
        - "name"
        - "price"
        - "sku"
        - "stockQuantity"
      properties:
        name:
          type: "string"
          example: "Wireless Mouse"
        description:
          type: "string"
          example: "A high-precision wireless optical mouse."
        price:
          type: "number"
          format: "float"
          minimum: 0
          example: 25.99
        sku:
          type: "string"
          example: "WM-102-BLK"
        stockQuantity:
          type: "integer"
          minimum: 0
          example: 150
    ProductUpdate:
      type: "object"
      properties:
        name:
          type: "string"
          example: "Premium Wireless Mouse"
        description:
          type: "string"
          example: "A high-precision wireless optical mouse with ergonomic design."
        price:
          type: "number"
          format: "float"
          minimum: 0
          example: 29.99
        stockQuantity:
          type: "integer"
          minimum: 0
          example: 120
    PaginatedProducts:
      allOf:
        - $ref: "#/components/schemas/PaginationInfo"
        - type: "object"
          properties:
            data:
              type: "array"
              items:
                $ref: "#/components/schemas/Product"

    # --- Cart Schemas ---
    CartItem:
      type: "object"
      properties:
        productId:
          type: "string"
          format: "uuid"
          example: "c7a1e3f4-5b6d-4c7a-8e9f-0a1b2c3d4e5f"
        productName:
          type: "string"
          example: "Wireless Mouse"
        quantity:
          type: "integer"
          example: 2
        pricePerUnit:
          type: "number"
          format: "float"
          example: 25.99
        totalPrice:
          type: "number"
          format: "float"
          example: 51.98
    Cart:
      type: "object"
      properties:
        items:
          type: "array"
          items:
            $ref: "#/components/schemas/CartItem"
        subtotal:
          type: "number"
          format: "float"
          example: 51.98
        totalItems:
          type: "integer"
          example: 2
    CartItemAdd:
      type: "object"
      required:
        - "productId"
        - "quantity"
      properties:
        productId:
          type: "string"
          format: "uuid"
          example: "c7a1e3f4-5b6d-4c7a-8e9f-0a1b2c3d4e5f"
        quantity:
          type: "integer"
          minimum: 1
          example: 1
    CartItemUpdate:
      type: "object"
      required:
        - "quantity"
      properties:
        quantity:
          type: "integer"
          minimum: 1
          example: 3

    # --- Order Schemas ---
    OrderItem:
      type: "object"
      properties:
        productId:
          type: "string"
          format: "uuid"
        productName:
          type: "string"
        quantity:
          type: "integer"
        pricePerUnit:
          type: "number"
          format: "float"
    ShippingAddress:
      type: "object"
      required:
        - "street"
        - "city"
        - "state"
        - "zipCode"
        - "country"
      properties:
        street:
          type: "string"
          example: "123 Main St"
        city:
          type: "string"
          example: "Anytown"
        state:
          type: "string"
          example: "CA"
        zipCode:
          type: "string"
          example: "12345"
        country:
          type: "string"
          example: "USA"
    Order:
      type: "object"
      properties:
        id:
          type: "string"
          format: "uuid"
          readOnly: true
          example: "e5a1e3f4-5b6d-4c7a-8e9f-0a1b2c3d4e5f"
        userId:
          type: "string"
          format: "uuid"
          readOnly: true
        items:
          type: "array"
          items:
            $ref: "#/components/schemas/OrderItem"
        totalAmount:
          type: "number"
          format: "float"
          example: 51.98
        status:
          type: "string"
          enum: ["pending", "processing", "shipped", "delivered", "cancelled"]
          example: "pending"
        shippingAddress:
          $ref: "#/components/schemas/ShippingAddress"
        createdAt:
          type: "string"
          format: "date-time"
          readOnly: true
        updatedAt:
          type: "string"
          format: "date-time"
          readOnly: true
    OrderCreate:
      type: "object"
      required:
        - "shippingAddress"
      properties:
        shippingAddress:
          $ref: "#/components/schemas/ShippingAddress"
    PaginatedOrders:
      allOf:
        - $ref: "#/components/schemas/PaginationInfo"
        - type: "object"
          properties:
            data:
              type: "array"
              items:
                $ref: "#/components/schemas/Order"
```
✅ Streaming completed.