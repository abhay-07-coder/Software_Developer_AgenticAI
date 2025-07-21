As a Senior Full-Stack Software Developer AI Agent, I will now address the task of "UI/UX Wireframing and Prototyping."

It's important to note that UI/UX design, including the creation of wireframes and prototypes in tools like Figma, is typically the responsibility of a dedicated UI/UX Designer. A developer's role is to implement these designs into functional software.

However, to fulfill the spirit of this request, I will provide the developer's equivalent of these artifacts. I will create:
1.  **User Flow Diagrams** using Mermaid.js, a text-based diagramming tool often used in developer documentation.
2.  **Low-Fidelity Wireframes** described in a structured text format, outlining the components and layout of each screen.
3.  A **High-Fidelity Clickable Prototype** implemented as a simple, unstyled but functional React application. This serves as an interactive, code-based wireframe that demonstrates user flows and application structure, fulfilling the "working code" requirement.

This approach provides a solid, tangible foundation that can be reviewed by the team, handed off to a designer for visual polishing, and used by developers as a scaffold for the final implementation.

## Architecture & Design of the Clickable Prototype

I will construct a Single Page Application (SPA) using **React** and **React Router**. This choice is ideal for creating a responsive and interactive user experience, which is the core of a clickable prototype.

-   **Component-Based Architecture**: Each screen (Home, Product List, etc.) and reusable element (Header) will be a separate React component. This promotes modularity and maintainability.
-   **Client-Side Routing**: `react-router-dom` will manage navigation between the different screens without requiring a full page reload, accurately simulating a modern web application's flow.
-   **State Management**: For this prototype, we'll use simple component state (`useState`) and prop drilling. For a full-scale application, a more robust solution like Redux Toolkit or React Context API would be integrated.
-   **Styling**: Minimal CSS will be used to create a "wireframe" aesthetic—grayscale, borders, and basic layouts—to focus on structure and functionality rather than visual design.
-   **Data**: Mock data will be used to populate the product lists and details, simulating API responses.

This architecture provides a clear and scalable foundation for the actual frontend development.

## User Flow Diagram

This diagram illustrates the primary path a user takes from landing on the site to completing a purchase.

```mermaid
graph TD
    A[Start: User visits site] --> B{Home Page};
    B --> C[View All Products];
    B --> D{Search for a product};
    D --> E[Product List Page];
    C --> E;
    E --> F{Select a Product};
    F --> G[Product Detail Page];
    G --> H{Add to Cart};
    H --> I[Shopping Cart Page];
    I --> J{Proceed to Checkout};
    J --> K[Checkout Page];
    K --> L{Enter Shipping & Payment Info};
    L --> M[Place Order];
    M --> N[Order Confirmation Page];
    N --> O[End];

    %% Alternative Flows
    G --> E;
    I --> E;
```

## Low-Fidelity Wireframes (Text-Based)

Here are the structural descriptions for each key screen.

### 1. Home Page
-   **Header**: [Logo] [Navigation Links: Home, Products, Cart] [Search Bar]
-   **Hero Section**: [Large promotional image or banner] [Call-to-Action Button: "Shop Now"]
-   **Featured Products Section**: [Section Title: "Featured Products"] [Grid of 4-8 Product Cards]
-   **Footer**: [Links: About Us, Contact, FAQ] [Social Media Icons]

### 2. Product List Page
-   **Header**: [Same as Home]
-   **Breadcrumbs**: [Home > Products]
-   **Sidebar (Filters)**: [Category Filter] [Price Range Slider] [Brand Filter]
-   **Main Content**:
    -   [Page Title: "All Products"]
    -   [Sort Dropdown: Price, Name, etc.]
    -   [Grid of Product Cards (paginated)]
    -   [Pagination Controls: Prev, 1, 2, 3, Next]
-   **Footer**: [Same as Home]

### 3. Product Detail Page
-   **Header**: [Same as Home]
-   **Breadcrumbs**: [Home > Products > Product Name]
-   **Main Content (Two-column layout)**:
    -   **Left Column**: [Main Product Image] [Thumbnail gallery of other images]
    -   **Right Column**: [Product Name] [Product Price] [Short Description] [Quantity Selector] [Add to Cart Button]
-   **Detailed Info Section**: [Tabs: Full Description, Specifications, Reviews]
-   **Footer**: [Same as Home]

### 4. Shopping Cart Page
-   **Header**: [Same as Home]
-   **Breadcrumbs**: [Home > Cart]
-   **Main Content**:
    -   [Page Title: "Your Shopping Cart"]
    -   [List of Cart Items]:
        -   Each item: [Product Image] [Product Name] [Price] [Quantity Selector] [Remove Button]
    -   **Order Summary**: [Subtotal] [Shipping (estimated)] [Total]
    -   [Proceed to Checkout Button]
-   **Footer**: [Same as Home]

### 5. Checkout Page
-   **Header**: [Simplified: Logo] [Secure Checkout]
-   **Main Content (Multi-step form or single page)**:
    -   **Shipping Information**: [Full Name] [Address] [City] [State] [ZIP Code]
    -   **Payment Information**: [Credit Card Number] [Expiration Date] [CVV] [Name on Card]
    -   **Order Review**: [List of items] [Final Total]
    -   [Place Order Button]
-   **Footer**: [Simplified: Security seals, links to privacy policy]

## High-Fidelity Clickable Prototype (React Implementation)

This is a complete, runnable React application that serves as a high-fidelity, interactive wireframe.

### 1. Dependencies

The following dependencies are required. They are listed in the `package.json` file.

-   `react`
-   `react-dom`
-   `react-router-dom`

### 2. Setup and Execution

1.  **Prerequisites**: Ensure you have Node.js and npm installed.
2.  **Create Project**: Use Create React App to bootstrap the project:
    ```bash
    npx create-react-app ecomm-prototype
    cd ecomm-prototype
    ```
3.  **Install Router**:
    ```bash
    npm install react-router-dom
    ```
4.  **Replace Files**: Replace the contents of the generated `src` and `public` directories with the files provided below.
5.  **Run the Prototype**:
    ```bash
    npm start
    ```
    The application will be available at `http://localhost:3000`.

### 3. Project File Structure

```
ecomm-prototype/
├── public/
│   └── index.html
├── src/
│   ├── components/
│   │   ├── CartPage.js
│   │   ├── CheckoutPage.js
│   │   ├── HomePage.js
│   │   ├── ProductDetailPage.js
│   │   ├── ProductListPage.js
│   │   └── common/
│   │       └── Header.js
│   ├── data/
│   │   └── products.js
│   ├── App.css
│   ├── App.js
│   └── index.js
└── package.json
```

---
### `package.json`

```json
{
  "name": "ecomm-prototype",
  "version": "0.1.0",
  "private": true,
  "dependencies": {
    "@testing-library/jest-dom": "^5.16.5",
    "@testing-library/react": "^13.4.0",
    "@testing-library/user-event": "^13.5.0",
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "react-router-dom": "^6.11.2",
    "react-scripts": "5.0.1",
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

### `public/index.html`

```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <link rel="icon" href="%PUBLIC_URL%/favicon.ico" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <meta name="theme-color" content="#000000" />
    <meta
      name="description"
      content="E-commerce Clickable Prototype"
    />
    <title>E-commerce Prototype</title>
  </head>
  <body>
    <noscript>You need to enable JavaScript to run this app.</noscript>
    <div id="root"></div>
  </body>
</html>
```

### `src/index.js`

```javascript
import React from 'react';
import ReactDOM from 'react-dom/client';
import { BrowserRouter } from 'react-router-dom';
import App from './App';
import './App.css';

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <BrowserRouter>
      <App />
    </BrowserRouter>
  </React.StrictMode>
);
```

### `src/App.css`

```css
/* Basic Wireframe Styling */
body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen',
    'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue',
    sans-serif;
  margin: 0;
  background-color: #f4f4f4;
  color: #333;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

/* Header */
.header {
  background-color: #fff;
  padding: 15px 30px;
  border-bottom: 2px solid #ddd;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.header .logo {
  font-weight: bold;
  font-size: 1.5em;
  color: #333;
  text-decoration: none;
}

.header nav a {
  margin: 0 15px;
  text-decoration: none;
  color: #555;
  font-weight: 500;
}

.header nav a:hover {
  color: #007bff;
}

/* General Page Styles */
.page-title {
  font-size: 2em;
  margin-bottom: 20px;
  border-bottom: 1px solid #ccc;
  padding-bottom: 10px;
}

/* Buttons */
.btn {
  display: inline-block;
  padding: 10px 20px;
  font-size: 1em;
  cursor: pointer;
  text-align: center;
  text-decoration: none;
  border: 1px solid #ccc;
  background-color: #e9e9e9;
  color: #333;
  border-radius: 4px;
}

.btn-primary {
  background-color: #007bff;
  color: white;
  border-color: #007bff;
}

.btn:hover {
  opacity: 0.9;
}

/* Forms */
.form-group {
  margin-bottom: 15px;
}

.form-group label {
  display: block;
  margin-bottom: 5px;
  font-weight: bold;
}

.form-group input {
  width: 100%;
  padding: 8px;
  box-sizing: border-box;
  border: 1px solid #ccc;
  border-radius: 4px;
}

/* Generic placeholder box */
.placeholder-box {
  background-color: #e0e0e0;
  border: 1px dashed #aaa;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #777;
  text-align: center;
}

/* Home Page */
.hero-section {
  height: 300px;
  margin-bottom: 40px;
}

/* Product List */
.product-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 20px;
}

.product-card {
  border: 1px solid #ddd;
  background-color: #fff;
  padding: 15px;
  text-align: center;
}

.product-card .product-image {
  height: 150px;
  width: 100%;
  margin-bottom: 15px;
}

.product-card h3 {
  margin: 10px 0;
  font-size: 1.1em;
}

.product-card a {
  text-decoration: none;
  color: inherit;
}

/* Product Detail */
.product-detail-layout {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 40px;
}

.product-detail-image {
  height: 400px;
  width: 100%;
}

/* Cart & Checkout */
.cart-item, .order-summary, .checkout-form {
  background-color: #fff;
  border: 1px solid #ddd;
  padding: 20px;
  margin-bottom: 20px;
}

.cart-item {
  display: flex;
  align-items: center;
  gap: 20px;
}

.cart-item-image {
  width: 80px;
  height: 80px;
}

.cart-item-details {
  flex-grow: 1;
}

.cart-total {
  text-align: right;
  font-size: 1.5em;
  font-weight: bold;
  margin-top: 20px;
}
```

### `src/App.js`

```javascript
import React from 'react';
import { Routes, Route } from 'react-router-dom';
import Header from './components/common/Header';
import HomePage from './components/HomePage';
import ProductListPage from './components/ProductListPage';
import ProductDetailPage from './components/ProductDetailPage';
import CartPage from './components/CartPage';
import CheckoutPage from './components/CheckoutPage';

function App() {
  // In a real app, cart state would be managed globally (Context API, Redux)
  // For this prototype, we pass it down from the top-level component.
  const [cartItems, setCartItems] = React.useState([]);

  const handleAddToCart = (product, quantity) => {
    // NOTE: This is a simplified add-to-cart logic for prototype purposes.
    // A real implementation would handle existing items and more complex state.
    setCartItems(prevItems => [...prevItems, { ...product, quantity }]);
    alert(`${product.name} added to cart!`);
  };

  return (
    <div className="App">
      <Header />
      <main className="container">
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/products" element={<ProductListPage />} />
          <Route 
            path="/products/:productId" 
            element={<ProductDetailPage onAddToCart={handleAddToCart} />} 
          />
          <Route path="/cart" element={<CartPage cartItems={cartItems} />} />
          <Route path="/checkout" element={<CheckoutPage />} />
        </Routes>
      </main>
    </div>
  );
}

export default App;
```

### `src/data/products.js`

```javascript
// Mock product data to simulate an API response
export const products = [
  {
    id: 1,
    name: 'Classic T-Shirt',
    price: 19.99,
    description: 'A comfortable and stylish classic t-shirt made from 100% premium cotton.',
    imageUrl: 't-shirt',
    category: 'Apparel',
  },
  {
    id: 2,
    name: 'Wireless Headphones',
    price: 99.99,
    description: 'High-fidelity wireless headphones with noise-cancellation and a 20-hour battery life.',
    imageUrl: 'headphones',
    category: 'Electronics',
  },
  {
    id: 3,
    name: 'Leather Wallet',
    price: 49.50,
    description: 'A sleek and durable leather wallet with multiple card slots and a cash compartment.',
    imageUrl: 'wallet',
    category: 'Accessories',
  },
  {
    id: 4,
    name: 'Running Shoes',
    price: 120.00,
    description: 'Lightweight and responsive running shoes designed for maximum comfort and performance.',
    imageUrl: 'shoes',
    category: 'Footwear',
  },
  {
    id: 5,
    name: 'Stainless Steel Water Bottle',
    price: 25.00,
    description: 'Keep your drinks cold for 24 hours or hot for 12 with this insulated water bottle.',
    imageUrl: 'bottle',
    category: 'Accessories',
  },
  {
    id: 6,
    name: 'Smartwatch',
    price: 249.99,
    description: 'Track your fitness, receive notifications, and more with this feature-packed smartwatch.',
    imageUrl: 'smartwatch',
    category: 'Electronics',
  },
];

export const getProductById = (id) => {
  // The '==' is intentional to handle string vs number from URL params
  return products.find(p => p.id == id);
};
```

### `src/components/common/Header.js`

```javascript
import React from 'react';
import { Link } from 'react-router-dom';

function Header() {
  return (
    <header className="header">
      <Link to="/" className="logo">
        PROTOTYPE
      </Link>
      <nav>
        <Link to="/">Home</Link>
        <Link to="/products">Products</Link>
        <Link to="/cart">Cart</Link>
      </nav>
    </header>
  );
}

export default Header;
```

### `src/components/HomePage.js`

```javascript
import React from 'react';
import { Link } from 'react-router-dom';

function HomePage() {
  return (
    <div>
      <div className="hero-section placeholder-box">
        <div>
          <h1>Hero Banner</h1>
          <p>Promotional content goes here.</p>
          <Link to="/products" className="btn btn-primary">Shop Now</Link>
        </div>
      </div>
      <h2 className="page-title">Featured Products</h2>
      <div className="product-grid">
        {/* In a real app, these would be fetched dynamically */}
        <div className="product-card placeholder-box">Product 1</div>
        <div className="product-card placeholder-box">Product 2</div>
        <div className="product-card placeholder-box">Product 3</div>
        <div className="product-card placeholder-box">Product 4</div>
      </div>
    </div>
  );
}

export default HomePage;
```

### `src/components/ProductListPage.js`

```javascript
import React from 'react';
import { Link } from 'react-router-dom';
import { products } from '../data/products';

function ProductListPage() {
  return (
    <div>
      <h1 className="page-title">All Products</h1>
      <div className="product-grid">
        {products.map(product => (
          <Link to={`/products/${product.id}`} key={product.id} className="product-card">
            <div className="product-image placeholder-box">{product.imageUrl}</div>
            <h3>{product.name}</h3>
            <p>${product.price.toFixed(2)}</p>
          </Link>
        ))}
      </div>
    </div>
  );
}

export default ProductListPage;
```

### `src/components/ProductDetailPage.js`

```javascript
import React, { useState } from 'react';
import { useParams } from 'react-router-dom';
import { getProductById } from '../data/products';

function ProductDetailPage({ onAddToCart }) {
  const { productId } = useParams();
  const product = getProductById(productId);
  const [quantity, setQuantity] = useState(1);

  if (!product) {
    return <div>Product not found!</div>;
  }

  const handleAddToCartClick = () => {
    // TODO: Add proper input validation for quantity
    if (quantity > 0) {
      onAddToCart(product, quantity);
    }
  };

  return (
    <div>
      <h1 className="page-title">{product.name}</h1>
      <div className="product-detail-layout">
        <div className="product-detail-image placeholder-box">
          {product.imageUrl}
        </div>
        <div>
          <h2>${product.price.toFixed(2)}</h2>
          <p>{product.description}</p>
          <div className="form-group">
            <label htmlFor="quantity">Quantity:</label>
            <input 
              type="number" 
              id="quantity" 
              value={quantity} 
              onChange={(e) => setQuantity(parseInt(e.target.value, 10))}
              min="1"
              style={{width: '60px'}}
            />
          </div>
          <button className="btn btn-primary" onClick={handleAddToCartClick}>
            Add to Cart
          </button>
        </div>
      </div>
    </div>
  );
}

export default ProductDetailPage;
```

### `src/components/CartPage.js`

```javascript
import React from 'react';
import { Link } from 'react-router-dom';

function CartPage({ cartItems }) {
  // NOTE: In a real app, cart logic (total, removal) would be more robust.
  const subtotal = cartItems.reduce((sum, item) => sum + item.price * item.quantity, 0);
  const shipping = subtotal > 0 ? 10.00 : 0; // Dummy shipping cost
  const total = subtotal + shipping;

  return (
    <div>
      <h1 className="page-title">Shopping Cart</h1>
      {cartItems.length === 0 ? (
        <p>Your cart is empty.</p>
      ) : (
        <>
          {cartItems.map((item, index) => (
            <div key={index} className="cart-item">
              <div className="cart-item-image placeholder-box">{item.imageUrl}</div>
              <div className="cart-item-details">
                <h3>{item.name}</h3>
                <p>Quantity: {item.quantity}</p>
              </div>
              <p>${(item.price * item.quantity).toFixed(2)}</p>
            </div>
          ))}
          <div className="order-summary">
            <h3>Order Summary</h3>
            <p>Subtotal: ${subtotal.toFixed(2)}</p>
            <p>Shipping: ${shipping.toFixed(2)}</p>
            <hr />
            <p className="cart-total">Total: ${total.toFixed(2)}</p>
          </div>
          <div style={{ textAlign: 'right' }}>
            <Link to="/checkout" className="btn btn-primary">
              Proceed to Checkout
            </Link>
          </div>
        </>
      )}
    </div>
  );
}

export default CartPage;
```

### `src/components/CheckoutPage.js`

```javascript
import React from 'react';

function CheckoutPage() {
  const handleSubmit = (e) => {
    e.preventDefault();
    // NOTE: This is where form submission logic would go.
    // In a real app, this would involve validation, API calls, and payment processing.
    alert('Order placed successfully! (This is a prototype)');
  };

  return (
    <div>
      <h1 className="page-title">Checkout</h1>
      <form onSubmit={handleSubmit} className="checkout-form">
        <h3>Shipping Information</h3>
        {/* TODO: Implement proper input validation and state management for form fields */}
        <div className="form-group">
          <label htmlFor="name">Full Name</label>
          <input type="text" id="name" required />
        </div>
        <div className="form-group">
          <label htmlFor="address">Address</label>
          <input type="text" id="address" required />
        </div>
        
        <h3 style={{marginTop: '30px'}}>Payment Information</h3>
        <div className="form-group">
          <label htmlFor="cc-number">Credit Card Number</label>
          <input type="text" id="cc-number" placeholder="XXXX XXXX XXXX XXXX" required />
        </div>

        <button type="submit" className="btn btn-primary" style={{width: '100%', marginTop: '20px'}}>
          Place Order
        </button>
      </form>
    </div>
  );
}

export default CheckoutPage;
```
✅ Streaming completed.