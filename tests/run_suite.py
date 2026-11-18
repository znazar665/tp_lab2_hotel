import sys
import os
import unittest

# Додаємо кореневу директорію проєкту до sys.path для коректного імпорту при прямому запуску
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.hotel_manager import HotelManager
from tests.test_hotel_manager import TestHotelManager
from tests.test_booking_service import TestBookingService


class TestHotelPlannedFeatures(unittest.TestCase):
    """Тести для функціоналу, який заплановано у наступних версіях (демонстрація декораторів)."""

    def setUp(self):
        self.hotel = HotelManager(total_rooms=5)

    @unittest.expectedFailure
    def test_vip_discount_not_implemented_yet(self):
        """Очікувана помилка: автоматична VIP-знижка 15% ще не реалізована в check_out."""
        self.hotel.check_in(room_number=1, guest_name="VIP Гість", days=2, price_per_day=1000.0)
        receipt = self.hotel.check_out(room_number=1)
        # Очікуємо 1700.0 зі знижкою, але метод повертає 2000.0 — тест зафіксує expectedFailure (x)
        self.assertEqual(receipt["total_cost"], 1700.0)


def create_full_test_suite() -> unittest.TestSuite:
    """Формування єдиного тестового набору (TestSuite) з усіх модулів проєкту."""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # Додаємо модульні тести основного класу HotelManager
    suite.addTests(loader.loadTestsFromTestCase(TestHotelManager))
    # Додаємо інтеграційні HTTP-тести мікросервісу FastAPI
    suite.addTests(loader.loadTestsFromTestCase(TestBookingService))
    # Додаємо тести із декоратором очікуваної помилки
    suite.addTests(loader.loadTestsFromTestCase(TestHotelPlannedFeatures))

    return suite


if __name__ == "__main__":
    full_suite = create_full_test_suite()
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(full_suite)
    sys.exit(not result.wasSuccessful())