def test_cache():
    SAMPLE_mod = SAMPLE.copy()
    region = regionprops(SAMPLE_mod)[0]
    f0 = region.filled_image
    region._label_image[:10] = 1
    f1 = region.filled_image
    assert_array_equal(f0, f1)
    region._cache_active = False
    f1 = region.filled_image
    assert np.any((f0 != f1))