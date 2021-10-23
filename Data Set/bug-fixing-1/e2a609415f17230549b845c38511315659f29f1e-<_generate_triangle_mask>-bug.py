

def _generate_triangle_mask(point, image, shape, random):
    'Generate a mask for a filled equilateral triangle shape.\n\n    The length of the sides of the triangle is generated randomly.\n\n    Parameters\n    ----------\n    point : tuple\n        The row and column of the top left corner of the rectangle.\n    image : tuple\n        The height, width and depth of the image into which the shape is placed.\n    shape : tuple\n        The minimum and maximum size and color of the shape to fit.\n    random : np.random.RandomState\n        The random state to use for random sampling.\n\n    Raises\n    ------\n    ArithmeticError\n        When a shape cannot be fit into the image with the given starting\n        coordinates. This usually means the image dimensions are too small or\n        shape dimensions too large.\n\n    Returns\n    -------\n    label : tuple\n        A (category, ((r0, r1), (c0, c1))) tuple specifying the category and\n        bounding box coordinates of the shape.\n    indices : 2-D array\n        A mask of indices that the shape fills.\n    '
    if ((shape[0] == 1) or (shape[1] == 1)):
        raise ValueError('dimension must be > 1 for circles')
    available_side = min((image[1] - point[1]), (point[0] + 1), shape[1])
    if (available_side < shape[0]):
        raise ArithmeticError('cannot fit shape to image')
    side = random.randint(shape[0], (available_side + 1))
    triangle_height = int(np.ceil((np.sqrt((3 / 4.0)) * side)))
    triangle = draw_polygon([point[0], (point[0] - triangle_height), point[0]], [point[1], (point[1] + (side // 2)), (point[1] + side)])
    label = ('triangle', (((point[0] - triangle_height), point[0]), (point[1], (point[1] + side))))
    return (triangle, label)
