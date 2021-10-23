

def test_setitem_preserves_views(self, data):
    assert (data[(- 1)] != data[0])
    view1 = data.view()
    view2 = data[:]
    data[0] = data[(- 1)]
    assert (view1[0] == data[(- 1)])
    assert (view2[0] == data[(- 1)])
