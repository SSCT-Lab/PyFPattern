

def test_far_expiration(self):
    'Cookie will expire when a distant expiration time is provided.'
    response = HttpResponse()
    response.set_cookie('datetime', expires=datetime(2038, 1, 1, 4, 5, 6))
    datetime_cookie = response.cookies['datetime']
    self.assertIn(datetime_cookie['expires'], ('Fri, 01 Jan 2038 04:05:06 GMT', 'Fri, 01 Jan 2038 04:05:07 GMT'))
