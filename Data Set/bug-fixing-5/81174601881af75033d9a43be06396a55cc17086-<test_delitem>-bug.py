def test_delitem(self):
    del self.frame['A']
    assert ('A' not in self.frame)