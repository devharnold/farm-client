# Farm-Client App

A backend API built with **FastAPI** to support a digital platform connecting farmers and clients. The system is envisioned to initially handle user authentication, product listings, orders, notifications, S3-based image uploads and support payments via M-pesa.

## 🔧 Tech Stack

* **FastAPI** (Python)
* **PostgreSQL** (via async)
* **JWT** (Authentication)
* **AWS S3** (Image storage)
* **boto3** (S3 integration)
* **daraja** (Mpesa API)
* **docker** (Containerize the App)

## 📂 Modules

### ✅ Completed

* Authentication
* User Service
* Farmer Service
* Order Service
* Products Service

### 🚧 In Progress

* Notifications Service
* Payments Integration
* S3-based Image Uploads

## 📦 Installation

```bash
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
```

## 🏃 Running the Server

```bash
uvicorn main:app --reload
```

## 🌍 API Base URL

`http://localhost:8000`

## ✍️ Author

Henry Arnold

## 📜 License

MIT
