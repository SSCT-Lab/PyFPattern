@pytest.mark.skipif(PY36, reason='order by value for Python<3.6')
def test_constructor_dict_order_by_values(self):
    d = {
        'b': self.ts2,
        'a': self.ts1,
    }
    frame = DataFrame(data=d)
    expected = DataFrame(data=d, columns=list('ab'))
    tm.assert_frame_equal(frame, expected)