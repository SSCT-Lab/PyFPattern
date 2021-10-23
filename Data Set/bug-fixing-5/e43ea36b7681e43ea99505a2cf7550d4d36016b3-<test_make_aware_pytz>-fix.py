@requires_pytz
def test_make_aware_pytz(self):
    self.assertEqual(timezone.make_naive(CET.localize(datetime.datetime(2011, 9, 1, 12, 20, 30)), CET), datetime.datetime(2011, 9, 1, 12, 20, 30))
    self.assertEqual(timezone.make_naive(pytz.timezone('Asia/Bangkok').localize(datetime.datetime(2011, 9, 1, 17, 20, 30)), CET), datetime.datetime(2011, 9, 1, 12, 20, 30))
    if PY36:
        self.assertEqual(timezone.make_naive(datetime.datetime(2011, 9, 1, 12, 20, 30), CET), datetime.datetime(2011, 9, 1, 19, 20, 30))
    else:
        with self.assertRaises(ValueError):
            timezone.make_naive(datetime.datetime(2011, 9, 1, 12, 20, 30), CET)