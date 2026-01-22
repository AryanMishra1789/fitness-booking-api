from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from zoneinfo import ZoneInfo

from ..database import get_db
from .. import models, schemas
from ..auth import get_current_user

router = APIRouter(tags=["Classes"])

IST = ZoneInfo("Asia/Kolkata")


def convert_to_ist(dt: datetime) -> datetime:
    if dt.tzinfo is None:                            # SQLite may return naive datetime; treat it as IST
        return dt.replace(tzinfo=IST)
    return dt.astimezone(IST)


@router.post("/classes", response_model=schemas.ClassResponse)
def create_class(
    payload: schemas.CreateClassRequest,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    dt_ist = convert_to_ist(payload.dateTime)
    if dt_ist < datetime.now(IST):
        raise HTTPException(status_code=400, detail="Class dateTime cannot be in the past")

    new_class = models.FitnessClass(
        name=payload.name,
        instructor=payload.instructor,
        date_time_ist=dt_ist,
        available_slots=payload.availableSlots,
    )
    db.add(new_class)
    db.commit()
    db.refresh(new_class)

    return schemas.ClassResponse(
        id=new_class.id,
        name=new_class.name,
        dateTime=convert_to_ist(new_class.date_time_ist),
        instructor=new_class.instructor,
        availableSlots=new_class.available_slots,
    )


@router.get("/classes", response_model=list[schemas.ClassResponse])
def get_classes(db: Session = Depends(get_db)):
    now = datetime.now(IST)

    classes = (
        db.query(models.FitnessClass)
        .order_by(models.FitnessClass.date_time_ist.asc())
        .all()
    )

    return [
        schemas.ClassResponse(
            id=c.id,
            name=c.name,
            dateTime=convert_to_ist(c.date_time_ist),
            instructor=c.instructor,
            availableSlots=c.available_slots,
        )
        for c in classes
        if convert_to_ist(c.date_time_ist) >= now
    ]
