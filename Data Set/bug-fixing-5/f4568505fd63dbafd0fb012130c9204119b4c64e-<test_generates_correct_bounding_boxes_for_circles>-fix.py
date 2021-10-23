def test_generates_correct_bounding_boxes_for_circles():
    (image, labels) = random_shapes((43, 44), max_shapes=1, min_size=20, max_size=20, shape='circle', min_pixel_intensity=1, random_seed=42)
    assert (len(labels) == 1)
    (label, bbox) = labels[0]
    assert (label == 'circle'), label
    crop = image[bbox[0][0]:bbox[0][1], bbox[1][0]:bbox[1][1]]
    assert ((crop >= 1).any() and (crop <= 255).any())
    image[bbox[0][0]:bbox[0][1], bbox[1][0]:bbox[1][1]] = 255
    assert (image == 255).all()