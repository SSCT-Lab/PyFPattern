def test_reorder_labels():
    lx = 70
    ly = 100
    (data, labels) = make_2d_syntheticdata(lx, ly)
    labels[(labels == 2)] = 4
    labels_bf = random_walker(data, labels, beta=90, mode='bf')
    assert (labels_bf[25:45, 40:60] == 2).all()
    assert (data.shape == labels.shape)
    return (data, labels_bf)