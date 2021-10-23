def test_2d_inactive():
    lx = 70
    ly = 100
    (data, labels) = make_2d_syntheticdata(lx, ly)
    labels[10:20, 10:20] = (- 1)
    labels[46:50, 33:38] = (- 2)
    labels = random_walker(data, labels, beta=90)
    assert (labels.reshape((lx, ly))[25:45, 40:60] == 2).all()
    assert (data.shape == labels.shape)
    return (data, labels)