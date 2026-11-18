from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from src.hotel_manager import HotelManager, HotelError

app = FastAPI(title="Hotel Booking Microservice", version="1.0.0")

# Ініціалізуємо менеджер готелю на 5 номерів для мікросервісу
hotel_db = HotelManager(total_rooms=5)


class BookingRequest(BaseModel):
    room_number: int = Field(..., ge=1, description="Номер кімнати")
    guest_name: str = Field(..., min_length=1, description="ПІБ гостя")
    days: int = Field(..., gt=0, description="Кількість днів проживання")
    price_per_day: float = Field(default=1000.0, gt=0, description="Ціна за добу")


class ExtendRequest(BaseModel):
    extra_days: int = Field(..., gt=0, description="Додаткові дні проживання")


@app.get("/rooms/available")
def get_available_rooms():
    """Отримати список вільних номерів."""
    return {"available_rooms": hotel_db.get_available_rooms()}


@app.post("/bookings", status_code=201)
def create_booking(booking: BookingRequest):
    """Забронювати та заселити гостя у номер."""
    try:
        record = hotel_db.check_in(
            room_number=booking.room_number,
            guest_name=booking.guest_name,
            days=booking.days,
            price_per_day=booking.price_per_day
        )
        return {"status": "booked", "room_number": booking.room_number, "details": record}
    except HotelError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))


@app.patch("/bookings/{room_number}/extend")
def extend_booking(room_number: int, req: ExtendRequest):
    """Продовжити термін проживання у вказаному номері."""
    try:
        updated_days = hotel_db.extend_stay(room_number=room_number, extra_days=req.extra_days)
        return {"room_number": room_number, "updated_days": updated_days}
    except HotelError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))


@app.delete("/bookings/{room_number}")
def cancel_or_checkout_booking(room_number: int):
    """Виселити гостя та отримати фінальний розрахунок."""
    try:
        receipt = hotel_db.check_out(room_number=room_number)
        return {"status": "checked_out", "receipt": receipt}
    except HotelError as e:
        raise HTTPException(status_code=404, detail=str(e))