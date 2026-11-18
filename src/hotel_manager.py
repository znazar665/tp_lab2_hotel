class HotelError(Exception):
    """Базовий виняток для операцій готелю."""
    pass


class HotelManager:
    def __init__(self, total_rooms: int = 10):
        if total_rooms <= 0:
            raise ValueError("Кількість номерів повинна бути більшою за нуль.")
        self.total_rooms = total_rooms
        # Словник активних гостей: {room_number: {"guest_name": str, "days": int, "price_per_day": float}}
        self.guests = {}

    def check_in(self, room_number: int, guest_name: str, days: int, price_per_day: float = 1000.0) -> dict:
        """Реєстрація (заселення) гостя в номер."""
        if not (1 <= room_number <= self.total_rooms):
            raise HotelError(f"Номер {room_number} не існує в готелі.")
        if room_number in self.guests:
            raise HotelError(f"Номер {room_number} вже зайнятий.")
        if not guest_name or not guest_name.strip():
            raise ValueError("Ім'я гостя не може бути порожнім.")
        if days <= 0:
            raise ValueError("Кількість днів проживання повинна бути додатньою.")
        if price_per_day <= 0:
            raise ValueError("Вартість за добу повинна бути додатньою.")

        record = {
            "guest_name": guest_name.strip(),
            "days": days,
            "price_per_day": price_per_day
        }
        self.guests[room_number] = record
        return record

    def extend_stay(self, room_number: int, extra_days: int) -> int:
        """Продовження проживання гостя на вказану кількість днів."""
        if room_number not in self.guests:
            raise HotelError(f"Номер {room_number} вільний, нікому продовжувати проживання.")
        if extra_days <= 0:
            raise ValueError("Кількість додаткових днів повинна бути більшою за нуль.")

        self.guests[room_number]["days"] += extra_days
        return self.guests[room_number]["days"]

    def check_out(self, room_number: int) -> dict:
        """Виселення гостя та розрахунок фінального чеку."""
        if room_number not in self.guests:
            raise HotelError(f"Номер {room_number} вже вільний.")

        guest_data = self.guests.pop(room_number)
        total_cost = guest_data["days"] * guest_data["price_per_day"]
        return {
            "room_number": room_number,
            "guest_name": guest_data["guest_name"],
            "days": guest_data["days"],
            "total_cost": total_cost
        }

    def get_available_rooms(self) -> list:
        """Повертає список вільних номерів."""
        return [r for r in range(1, self.total_rooms + 1) if r not in self.guests]