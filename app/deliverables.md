# 📦 Deliverables

## ✅ Completed Modules

### 1. **Authentication**

* Implemented JWT-based authentication with FastAPI
* Included signup, login, and logout flows
* Applied secure password hashing techniques

### 2. **User Service**

* Full CRUD support for user records
* Enforced role-based access control for different endpoints

### 3. **Farmer Service**

* Enabled farmer profile creation and management
* Built out foundational business logic

### 4. **Order Service**

* Implemented order placement and status tracking
* Established farmer–buyer relationships

### 5. **Products Service**

* Added product CRUD features
* Linked products to respective farmer profiles
* Captured metadata in preparation for image storage

## 🚧 Pending Work

### 6. **Notifications**

* Implement order updates via email and/or in-app notifications

### 7. **Payments**

* Integrate M-Pesa or card-based payment methods
* Implement payment tracking and status feedback

### 8. **S3 Integration**

* Use `boto3` to support AWS S3 uploads
* Refactor `FarmerService` and `ProductService` to support media
* Modify business logic and APIs to store and return S3 URLs
