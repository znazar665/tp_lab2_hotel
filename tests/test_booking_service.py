import unittest
from fastapi.testclient import TestClient
from src.booking_service import app, hotel_db


class TestBookingService(unittest.TestCase):
    def setUp(self):
        """Очищення стану готелю перед кожним HTTP-тестом."""
        hotel_db.guests.clear()
        self.client = TestClient(app)

    def test_get_initial_available_rooms(self):
        """Перевірка GET /rooms/available для порожнього готелю."""
        response = self.client.get("/rooms/available")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"available_rooms": [1, 2, 3, 4, 5]})

    def test_create_booking_success(self):
        """Перевірка успішного бронювання через POST /bookings."""
        payload = {
            "room_number": 2,
            "guest_name": "Дмитро Мельник",
            "days": 4,
            "price_per_day": 1500.0
        }
        response = self.client.post("/bookings", json=payload)
        self.assertEqual(response.status_code, 201)
        data = response.json()
        self.assertEqual(data["status"], "booked")
        self.assertEqual(data["room_number"], 2)
        self.assertEqual(data["details"]["guest_name"], "Дмитро Мельник")

    def test_create_booking_occupied_room_returns_400(self):
        """Перевірка помилки 400 при спробі повторно забронювати зайнятий номер."""
        payload = {"room_number": 1, "guest_name": "Олена Сидоренко", "days": 2}
        self.client.post("/bookings", json=payload)

        duplicate_response = self.client.post("/bookings", json=payload)
        self.assertEqual(duplicate_response.status_code, 400)
        self.assertIn("вже зайнятий", duplicate_response.json()["detail"])

    def test_extend_booking_success(self):
        """Перевірка продовження бронювання через PATCH /bookings/{room_number}/extend."""
        self.client.post("/bookings", json={"room_number": 3, "guest_name": "Андрій Кравчук", "days": 2})

        response = self.client.patch("/bookings/3/extend", json={"extra_days": 3})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["updated_days"], 5)

    def test_checkout_booking_and_receipt(self):
        """Перевірка виселення через DELETE /bookings/{room_number} та розрахунку чеку."""
        self.client.post("/bookings", json={
            "room_number": 4,
            "guest_name": "Ірина Ткаченко",
            "days": 3,
            "price_per_day": 2000.0
        })

        response = self.client.delete("/bookings/4")
        self.assertEqual(response.status_code, 200)
        receipt = response.json()["receipt"]
        self.assertEqual(receipt["total_cost"], 6000.0)

        # Переконуємося, що номер 4 знову у списку вільних
        avail = self.client.get("/rooms/available").json()["available_rooms"]
        self.assertIn(4, avail)

    def test_checkout_nonexistent_booking_returns_404(self):
        """Перевірка статусу 404 при спробі виселити порожній номер."""
        response = self.client.delete("/bookings/5")
        self.assertEqual(response.status_code, 404)


if __name__ == "__main__":
    unittest.main()