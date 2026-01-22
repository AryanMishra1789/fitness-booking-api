import logging
from fastapi import FastAPI

from .database import Base, engine
from . import models  # noqa: F401 (ensures models are registered before create_all)
from .routers import auth_routes, class_routes, booking_routes

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)
logger = logging.getLogger(__name__)

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Fitness Booking API", version="1.0.0")

app.include_router(auth_routes.router)
app.include_router(class_routes.router)
app.include_router(booking_routes.router)


@app.get("/")
def health():
    logger.info("Health check called")
    return {"status": "ok"}
