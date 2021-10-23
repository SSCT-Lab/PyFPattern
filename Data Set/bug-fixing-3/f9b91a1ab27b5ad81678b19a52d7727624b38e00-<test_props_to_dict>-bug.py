def test_props_to_dict():
    regions = regionprops(SAMPLE)
    out = _props_to_dict(regions)
    assert (out == {
        'label': array([1]),
        'bbox-0': array([0]),
        'bbox-1': array([0]),
        'bbox-2': array([10]),
        'bbox-3': array([18]),
    })
    regions = regionprops(SAMPLE)
    out = _props_to_dict(regions, properties=('label', 'area', 'bbox'), separator='+')
    assert (out == {
        'label': array([1]),
        'area': array([180]),
        'bbox+0': array([0]),
        'bbox+1': array([0]),
        'bbox+2': array([10]),
        'bbox+3': array([18]),
    })