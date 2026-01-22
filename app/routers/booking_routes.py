from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from zoneinfo import ZoneInfo

from ..database import get_db
from .. import models, schemas
from ..auth import get_current_user

router = APIRouter(tags=["Bookings"])

IST = ZoneInfo("Asia/Kolkata")


def ensure_ist_aware(dt: datetime) -> datetime:
    """SQLite may return naive datetime; treat it as IST."""
    if dt.tzinfo is None:
        return dt.replace(tzinfo=IST)
    return dt.astimezone(IST)


@router.post("/book", response_model=schemas.BookClassResponse)
def book_class(
    payload: schemas.CreateBookingRequest,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    fitness_class = (
        db.query(models.FitnessClass)
        .filter(models.FitnessClass.id == payload.class_id)
        .first()
    )
    if not fitness_class:
        raise HTTPException(status_code=404, detail="Class not found")

    # Prevent booking past class
    class_time = ensure_ist_aware(fitness_class.date_time_ist)
    if class_time < datetime.now(IST):
        raise HTTPException(status_code=400, detail="Cannot book past class")

    # Prevent duplicate booking
    existing = (
        db.query(models.Booking)
        .filter(models.Booking.user_id == user.id, models.Booking.class_id == payload.class_id)
        .first()
    )
    if existing:
        raise HTTPException(status_code=409, detail="Already booked this class")

    # Prevent overbooking
    if fitness_class.available_slots <= 0:
        raise HTTPException(status_code=400, detail="No slots available")

    try:
        fitness_class.available_slots -= 1

        booking = models.Booking(
            user_id=user.id,
            class_id=payload.class_id,
            client_name=payload.client_name,
            client_email=payload.client_email,
        )
        db.add(booking)
        db.commit()
        db.refresh(booking)

        return schemas.BookClassResponse(
            message="Booking successful",
            booking_id=booking.id,
            remaining_slots=fitness_class.available_slots,
        )

    except Exception:
        db.rollback()
        raise HTTPException(status_code=500, detail="Booking failed")


@router.get("/bookings", response_model=list[schemas.BookingItem])
def get_bookings(
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    bookings = (
        db.query(models.Booking)
        .filter(models.Booking.user_id == user.id)
        .order_by(models.Booking.id.desc())
        .all()
    )

    return [
        schemas.BookingItem(
            booking_id=b.id,
            class_id=b.class_id,
            class_name=b.fitness_class.name,
            instructor=b.fitness_class.instructor,
            dateTime=ensure_ist_aware(b.fitness_class.date_time_ist),
            client_name=b.client_name,
            client_email=b.client_email,
        )
        for b in bookings
    ]