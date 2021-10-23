def test_P22():
    d = 100
    M = ((2 - x) * eye(d))
    assert (M.eigenvals() == {
        ((- x) + 2): d,
    })