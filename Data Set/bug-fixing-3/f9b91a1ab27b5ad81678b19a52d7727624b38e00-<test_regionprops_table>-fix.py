def test_regionprops_table():
    out = regionprops_table(SAMPLE)
    assert (out == {
        'label': array([1]),
        'bbox-0': array([0]),
        'bbox-1': array([0]),
        'bbox-2': array([10]),
        'bbox-3': array([18]),
    })
    out = regionprops_table(SAMPLE, properties=('label', 'area', 'bbox'), separator='+')
    assert (out == {
        'label': array([1]),
        'area': array([72]),
        'bbox+0': array([0]),
        'bbox+1': array([0]),
        'bbox+2': array([10]),
        'bbox+3': array([18]),
    })