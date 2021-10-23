def test_throws_when_min_pixel_intensity_out_of_range():
    with testing.raises(ValueError):
        random_shapes((1000, 1234), max_shapes=1, min_pixel_intensity=256)
    with testing.raises(ValueError):
        random_shapes((2, 2), max_shapes=1, min_pixel_intensity=(- 1))