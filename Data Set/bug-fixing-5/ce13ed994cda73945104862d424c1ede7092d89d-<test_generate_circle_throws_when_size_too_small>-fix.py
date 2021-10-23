def test_generate_circle_throws_when_size_too_small():
    with testing.raises(ValueError):
        random_shapes((64, 128), max_shapes=1, min_size=1, max_size=1, shape='circle')