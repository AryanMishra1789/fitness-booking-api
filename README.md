# Fitness Studio Booking API (FastAPI)

A simple **Booking API** for a fictional fitness studio offering classes like **Yoga, Zumba, HIIT**, etc.  
Built using **Python + FastAPI + SQLite + JWT Authentication**.

---

## Features

- User authentication (Signup/Login) using JWT
- Create fitness classes (authenticated)
- View all upcoming fitness classes
- Book a class slot (authenticated)
- Prevents duplicate bookings
- Prevents overbooking & deducts slots after successful booking
- View bookings for authenticated user
- Timezone handling: class time stored and returned in **IST (Asia/Kolkata)**

---

## Tech Stack

- Python 3.11+
- FastAPI
- SQLite
- SQLAlchemy ORM
- JWT Authentication (OAuth2PasswordBearer)
- Swagger API Docs

---

## Setup Instructions (Local)

### 1) Clone the repository
```bash
git clone <YOUR_GITHUB_REPO_URL>
cd fitness_booking_api
```

### 2) Create & activate a virtual environment

#### Windows
```bash
python -m venv venv
venv\Scripts\activate
```

#### Mac/Linux
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3) Install dependencies
```bash
pip install -r requirements.txt
```

### 4) Run the server
```bash
uvicorn app.main:app --reload
```

Server will start at:

- [http://127.0.0.1:8000](http://127.0.0.1:8000)

Swagger Docs:

- [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

## Authentication

After login, you receive an access token.

For protected endpoints, include the token like this:

```
Authorization: Bearer <TOKEN>
```

Note: Access tokens expire after a fixed duration for security.

---

## API Endpoints

### 1) Sign Up
**POST** `/signup`

**Request:**
```json
{
  "name": "Aryan Mishra",
  "email": "aryan@gmail.com",
  "password": "aryan123"
}
```

**Response:**
```json
{
  "message": "Signup successful"
}
```

### 2) Login (Swagger Authorize)
**POST** `/login`

This endpoint accepts form-data and is mainly used by Swagger OAuth2 "Authorize".

In Swagger:

- Open `/docs`
- Click **Authorize**
- Enter:
  - `username` = your email
  - `password` = your password

### 3) Login JSON (Postman / curl / PowerShell)
**POST** `/login-json`

**Request:**
```json
{
  "email": "aryan@gmail.com",
  "password": "aryan123"
}
```

**Response:**
```json
{
  "access_token": "xxxxx",
  "token_type": "bearer"
}
```

### 4) Create a Class (Authenticated)
**POST** `/classes`

**Request:**
```json
{
  "name": "Yoga Flow",
  "dateTime": "2026-02-10T10:00:00Z",
  "instructor": "John Doe",
  "availableSlots": 5
}
```

**Response:**
```json
{
  "id": 1,
  "name": "Yoga Flow",
  "dateTime": "2026-02-10T15:30:00+05:30",
  "instructor": "John Doe",
  "availableSlots": 5
}
```

### 5) Get Upcoming Classes
**GET** `/classes`

**Response:**
```json
[
  {
    "id": 1,
    "name": "Yoga Flow",
    "dateTime": "2026-02-10T15:30:00+05:30",
    "instructor": "John Doe",
    "availableSlots": 5
  }
]
```

### 6) Book a Class (Authenticated)
**POST** `/book`

**Request:**
```json
{
  "class_id": 1,
  "client_name": "Aryan Mishra",
  "client_email": "aryan@gmail.com"
}
```

**Response:**
```json
{
  "message": "Booking successful",
  "booking_id": 1,
  "remaining_slots": 4
}
```

### 7) Get My Bookings (Authenticated)
**GET** `/bookings`

**Response:**
```json
[
  {
    "booking_id": 1,
    "class_id": 1,
    "class_name": "Yoga Flow",
    "dateTime": "2026-02-10T15:30:00+05:30",
    "instructor": "John Doe",
    "client_name": "Aryan Mishra",
    "client_email": "aryan@gmail.com"
  }
]
```

---

## Common Validations / Errors

- **401 Unauthorized** → Missing/invalid token
- **404 Not Found** → Class not found
- **409 Conflict** → Duplicate booking prevented
- **400 Bad Request** → No slots available / booking past class
- **422 Validation Error** → Missing fields / invalid request body

---

## Notes

- All class times are stored and returned in IST (Asia/Kolkata).
- Swagger UI is available at `/docs` and can be used to test the API easily.

---

## Running Unit Tests

Run tests using:

```bash
python -m pytest -q
```

Tests cover:

- Authentication flow (signup/login)
- Protected endpoint authorization
- Booking slot deduction
- Duplicate booking prevention

---

## Postman Collection

Postman collection file:
`postman/FitnessBookingAPI.postman_collection.json`

Note: Protected endpoints require header:
`Authorization: Bearer <TOKEN>` (token from `/login-json`)