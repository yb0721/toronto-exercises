import unittest
import bikes as pf

class TestBikes(unittest.TestCase):
    """测试bikes内的函数"""

    def test_get_station_info(self):
        """测试函数get_station_info"""

        expected = ['Danforth/Coxwell', 13, 2]
        result = pf.get_station_info(7088, pf.SAMPLE_STATIONS)
        self.assertEqual(expected,result)

    def test_get_total(self):
        """测试函数get_total"""

        excepted = 22
        result = pf.get_total(pf.BIKES_AVAILABLE, pf.SAMPLE_STATIONS)
        self.assertEqual(excepted,result)

    def test_get_stations_with_n_docks(self):
        """测试函数get_stations_with_n_docks"""

        expected = [7087, 7088]
        result = pf.get_stations_with_n_docks(2, pf.SAMPLE_STATIONS)
        self.assertEqual(expected,result)

    def test_get_direction(self):
        """测试函数get_direction"""

        expected = 'SOUTHWEST'
        result = pf.get_direction(7087, 7088, pf.SAMPLE_STATIONS)
        self.assertEqual(expected,result)

    def test_rent_bike(self):
        """测试函数rent_bike"""

        expected = True
        result = pf.rent_bike(7087, pf.SAMPLE_STATIONS)
        self.assertEqual(expected,result)

    def test_return_bike(self):
        """测试函数return_bike"""

        expected = True
        result = pf.rent_bike(7087, pf.SAMPLE_STATIONS)
        self.assertEqual(expected,result)

    def test_balance_all_bikes(self):
        """测试函数balance_all_bikes"""

        expected = 0
        result = pf.balance_all_bikes(pf.HANDOUT_STATIONS)
        self.assertEqual(expected,result)

unittest.main()