from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from datetime import datetime, timezone

from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

    bookings = relationship("Booking", back_populates="user", cascade="all, delete-orphan")


class FitnessClass(Base):
    __tablename__ = "classes"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(120), nullable=False)
    date_time_ist = Column(DateTime, nullable=False)  # stored in IST
    instructor = Column(String(120), nullable=False)
    available_slots = Column(Integer, nullable=False)

    bookings = relationship("Booking", back_populates="fitness_class", cascade="all, delete-orphan")


class Booking(Base):
    __tablename__ = "bookings"

    __table_args__ = (
        UniqueConstraint("user_id", "class_id", name="uq_user_class_booking"),
    )

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    class_id = Column(Integer, ForeignKey("classes.id"), nullable=False)

    client_name = Column(String(120), nullable=False)
    client_email = Column(String(255), nullable=False)

    booked_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

    user = relationship("User", back_populates="bookings")
    fitness_class = relationship("FitnessClass", back_populates="bookings")
