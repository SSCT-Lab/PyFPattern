@XFAIL
def test_M15():
    n = Dummy('n')
    assert (solveset((sin(x) - S.Half)) in (Union(ImageSet(Lambda(n, (((2 * n) * pi) + (pi / 6))), S.Integers), ImageSet(Lambda(n, (((2 * n) * pi) + ((5 * pi) / 6))), S.Integers)), Union(ImageSet(Lambda(n, (((2 * n) * pi) + ((5 * pi) / 6))), S.Integers), ImageSet(Lambda(n, (((2 * n) * pi) + (pi / 6))), S.Integers))))