import unittest
from src.hotel_manager import HotelManager, HotelError


class TestHotelManager(unittest.TestCase):
    def setUp(self):
        """Підготовка тестового середовища перед кожним тестом."""
        self.hotel = HotelManager(total_rooms=5)
        self.hotel.check_in(room_number=1, guest_name="Олександр Коваленко", days=3, price_per_day=1200.0)

    def test_successful_check_in(self):
        """Перевірка успішного заселення у вільний номер."""
        record = self.hotel.check_in(room_number=2, guest_name="Марія Бондаренко", days=2, price_per_day=1500.0)
        self.assertEqual(record["guest_name"], "Марія Бондаренко")
        self.assertEqual(record["days"], 2)
        self.assertNotIn(2, self.hotel.get_available_rooms())

    def test_check_in_occupied_room_raises_error(self):
        """Перевірка винятку при спробі заселення у вже зайнятий номер."""
        with self.assertRaises(HotelError):
            self.hotel.check_in(room_number=1, guest_name="Іван Петренко", days=1)

    def test_check_in_invalid_room_number(self):
        """Перевірка винятку при введенні неіснуючого номера кімнати."""
        with self.assertRaises(HotelError):
            self.hotel.check_in(room_number=99, guest_name="Іван Петренко", days=1)

    def test_check_in_invalid_input_values(self):
        """Перевірка валідації порожнього імені та некоректних днів."""
        with self.assertRaises(ValueError):
            self.hotel.check_in(room_number=3, guest_name="   ", days=2)
        with self.assertRaises(ValueError):
            self.hotel.check_in(room_number=3, guest_name="Тарас Шевченко", days=0)

    def test_extend_stay_success(self):
        """Перевірка коректного продовження проживання."""
        new_days = self.hotel.extend_stay(room_number=1, extra_days=4)
        self.assertEqual(new_days, 7)
        self.assertEqual(self.hotel.guests[1]["days"], 7)

    def test_extend_stay_empty_room(self):
        """Перевірка помилки при спробі продовжити проживання у вільному номері."""
        with self.assertRaises(HotelError):
            self.hotel.extend_stay(room_number=4, extra_days=2)

    def test_check_out_success_and_bill_calculation(self):
        """Перевірка виселення, розрахунку вартості та звільнення номера."""
        receipt = self.hotel.check_out(room_number=1)
        self.assertEqual(receipt["guest_name"], "Олександр Коваленко")
        self.assertEqual(receipt["total_cost"], 3600.0)
        self.assertIn(1, self.hotel.get_available_rooms())

    def test_check_out_empty_room_raises_error(self):
        """Перевірка помилки при виселенні з уже вільного номера."""
        with self.assertRaises(HotelError):
            self.hotel.check_out(room_number=5)


if __name__ == "__main__":
    unittest.main()