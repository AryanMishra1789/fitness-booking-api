from pydantic import BaseModel, EmailStr, Field
from datetime import datetime


# ---------- AUTH ----------
class SignupRequest(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    email: EmailStr
    password: str = Field(min_length=6, max_length=72)  # bcrypt safe limit

class SignupResponse(BaseModel):
    message: str


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


# ---------- CLASSES ----------
class CreateClassRequest(BaseModel):
    name: str = Field(min_length=2, max_length=120)
    dateTime: datetime
    instructor: str = Field(min_length=2, max_length=120)
    availableSlots: int = Field(gt=0, le=500)


class ClassResponse(BaseModel):
    id: int
    name: str
    dateTime: datetime
    instructor: str
    availableSlots: int


# ---------- BOOKINGS ----------
class CreateBookingRequest(BaseModel):
    # gt=0 ensures class_id must be a positive integer
    # example=1 makes Swagger docs show a realistic sample value
    class_id: int = Field(gt=0, json_schema_extra={"example": 1})
    client_name: str = Field(min_length=2, max_length=120)
    client_email: EmailStr


class BookClassResponse(BaseModel):
    message: str
    booking_id: int
    remaining_slots: int


class BookingItem(BaseModel):
    booking_id: int
    class_id: int
    class_name: str
    dateTime: datetime
    instructor: str
    client_name: str
    client_email: EmailStr
