import unittest
from file import WorkTime, td



class TestWorkTime(unittest.TestCase):

    def setUp(self):
        self.wk = WorkTime(start="06:30:00", end="14:51:00")
    
    def test_timedelta_(self):
        #Test avec les horaires fixes
        self.assertEqual(self.wk.timedelta_(), td(hours=7, minutes=36))
        self.assertEqual(self.wk.timedelta_("06:30:00", "15:51:00"), td(hours=8, minutes=36))
        self.assertEqual(self.wk.timedelta_("14:51:00", "00:09:00"), td(hours=8, minutes=30))
        #Test avec les d'autres horaires comme des retards
        self.assertEqual(self.wk.timedelta_("08:45:25", "15:51:00"), td(hours=6, minutes=20, seconds=35))
        self.assertEqual(self.wk.timedelta_("15:51:00", "15:51:00"), td(hours=0, minutes=0, seconds=0))
            #No break time
        self.assertEqual(self.wk.timedelta_("14:45:00", "14:51:00"), td(hours=0, minutes=6))
    
    def test_hrs_2dates(self):
        self.assertEqual(self.wk.hrs_2dates("05-04-23", "06-04-23"), "7:36:00")
        self.assertEqual(self.wk.hrs_2dates("04-01-23", "25-12-23"), "2614:24:00")
        # self.assertEqual(self.wk.hrs_2dates("05-04-23", "15-04-23"), "41:39:00")

    
    def test_error_raised(self):
        with self.assertRaises(AssertionError):
            WorkTime(start="06:30:00", end="16:00:00")

if __name__ == '__main__':
    unittest.main()



