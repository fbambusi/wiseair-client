import unittest
from wiseair.WiseairClient import WiseairUtils
import datetime
class MyTestCase(unittest.TestCase):
    def test_sleeping_livelinees(self):
        pot={"interval_between_measures_in_seconds":3600,"beginning_sleep_hour":23,"end_sleep_hour":5}
        last_measure={"created_at":"2020-01-10 23:00:00"}
        moment=datetime.datetime.strptime("2020-01-11 02:00:00",WiseairUtils.MEASURES_FORMAT_STRING)
        self.assertEqual(WiseairUtils.is_pot_alive(pot,last_measure,moment), True)

    def test_awake_livelinees(self):
        pot={"interval_between_measures_in_seconds":3600,"beginning_sleep_hour":23,"end_sleep_hour":5}
        last_measure={"created_at":"2020-01-10 22:00:00"}
        moment=datetime.datetime.strptime("2020-01-10 22:10:00",WiseairUtils.MEASURES_FORMAT_STRING)
        self.assertEqual(WiseairUtils.is_pot_alive(pot,last_measure,moment), True)

    def test_awake_death(self):
        pot = {"interval_between_measures_in_seconds": 3600, "beginning_sleep_hour": 23, "end_sleep_hour": 5}
        last_measure = {"created_at": "2020-01-10 20:00:00"}
        moment = datetime.datetime.strptime("2020-01-10 22:10:00", WiseairUtils.MEASURES_FORMAT_STRING)
        self.assertEqual(WiseairUtils.is_pot_alive(pot, last_measure, moment), False)

    def test_asleep_dead(self):
        pot = {"interval_between_measures_in_seconds": 3600, "beginning_sleep_hour": 23, "end_sleep_hour": 5}
        last_measure = {"created_at": "2020-01-10 20:00:00"}
        moment = datetime.datetime.strptime("2020-01-10 23:10:00", WiseairUtils.MEASURES_FORMAT_STRING)
        self.assertEqual(WiseairUtils.is_pot_alive(pot, last_measure, moment), False)

if __name__ == '__main__':
    unittest.main()
