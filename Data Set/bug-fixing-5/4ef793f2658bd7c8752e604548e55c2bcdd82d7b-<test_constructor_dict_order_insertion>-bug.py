@pytest.mark.skipif((not PY36), reason='Insertion order for Python>=3.6')
def test_constructor_dict_order_insertion(self):
    d = {
        'b': self.ts2,
        'a': self.ts1,
    }
    frame = DataFrame(data=d)
    expected = DataFrame(data=d, columns=list('ba'))
    tm.assert_frame_equal(frame, expected)