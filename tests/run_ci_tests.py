import sys
import os
import unittest
import xmlrunner

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from tests.test_hotel_manager import TestHotelManager
from tests.test_booking_service import TestBookingService


if __name__ == "__main__":
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    suite.addTests(loader.loadTestsFromTestCase(TestHotelManager))
    suite.addTests(loader.loadTestsFromTestCase(TestBookingService))

    runner = xmlrunner.XMLTestRunner(output='test-reports')
    result = runner.run(suite)
    sys.exit(not result.wasSuccessful())
