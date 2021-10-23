def test_generate_triangle_throws_when_size_too_small():
    with testing.raises(ValueError):
        random_shapes((128, 64), max_shapes=1, min_size=1, max_size=1, shape='triangle')