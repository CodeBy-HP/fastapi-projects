 Product Inventory API 🛒

Problem Statement:
Build an Inventory Management API to track products in a store.

Fields:

name: str
category: str
price: float
quantity: int
in_stock: bool (auto = quantity > 0)

Endpoints:
POST /products/ → Add product
GET /products/ → List products
GET /products/{id} → Get one product
PUT /products/{id} → Update product
DELETE /products/{id} → Remove product

🎯 Concepts Covered: CRUD, computed fields, simple business logic.
💡 Slightly more logical (because of in_stock auto-calculation).