def test_2d_bf():
    lx = 70
    ly = 100
    (data, labels) = make_2d_syntheticdata(lx, ly)
    labels_bf = random_walker(data, labels, beta=90, mode='bf')
    assert (labels_bf[25:45, 40:60] == 2).all()
    assert (data.shape == labels.shape)
    full_prob_bf = random_walker(data, labels, beta=90, mode='bf', return_full_prob=True)
    assert (full_prob_bf[1, 25:45, 40:60] >= full_prob_bf[0, 25:45, 40:60]).all()
    assert (data.shape == labels.shape)
    labels[(55, 80)] = 3
    full_prob_bf = random_walker(data, labels, beta=90, mode='bf', return_full_prob=True)
    assert (full_prob_bf[1, 25:45, 40:60] >= full_prob_bf[0, 25:45, 40:60]).all()
    assert (len(full_prob_bf) == 3)
    assert (data.shape == labels.shape)