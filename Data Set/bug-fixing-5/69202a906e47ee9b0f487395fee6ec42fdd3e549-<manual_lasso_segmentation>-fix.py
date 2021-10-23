def manual_lasso_segmentation(image, alpha=0.4, return_all=False):
    'Return a label image based on freeform selections made with the mouse.\n\n    Parameters\n    ----------\n    image : (M, N[, 3]) array\n        Grayscale or RGB image.\n\n    alpha : float, optional\n        Transparency value for polygons drawn over the image.\n\n    return_all : bool, optional\n        If True, an array containing each separate polygon drawn is returned.\n        (The polygons may overlap.) If False (default), latter polygons\n        "overwrite" earlier ones where they overlap.\n\n    Returns\n    -------\n    labels : array of int, shape ([Q, ]M, N)\n        The segmented regions. If mode is `\'separate\'`, the leading dimension\n        of the array corresponds to the number of regions that the user drew.\n\n    Notes\n    -----\n    Press and hold the left mouse button to draw around each object.\n\n    Examples\n    --------\n    >>> from skimage import data, future, io\n    >>> camera = data.camera()\n    >>> mask = future.manual_lasso_segmentation(camera)  # doctest: +SKIP\n    >>> io.imshow(mask)  # doctest: +SKIP\n    >>> io.show()  # doctest: +SKIP\n    '
    import matplotlib.pyplot as plt
    list_of_vertex_lists = []
    polygons_drawn = []
    if (image.ndim not in (2, 3)):
        raise ValueError('Only 2D grayscale or RGB images are supported.')
    (fig, ax) = plt.subplots()
    fig.subplots_adjust(bottom=0.2)
    ax.imshow(image, cmap='gray')
    ax.set_axis_off()

    def _undo(*args, **kwargs):
        if list_of_vertex_lists:
            list_of_vertex_lists.pop()
            last_poly = polygons_drawn.pop()
            last_poly.remove()
            fig.canvas.draw_idle()
    undo_pos = fig.add_axes([0.85, 0.05, 0.075, 0.075])
    undo_button = matplotlib.widgets.Button(undo_pos, '⟲')
    undo_button.on_clicked(_undo)

    def _on_lasso_selection(vertices):
        if (len(vertices) < 3):
            return
        list_of_vertex_lists.append(vertices)
        polygon_object = _draw_polygon(ax, vertices, alpha=alpha)
        polygons_drawn.append(polygon_object)
        plt.draw()
    lasso = matplotlib.widgets.LassoSelector(ax, _on_lasso_selection)
    plt.show(block=True)
    labels = (_mask_from_vertices(vertices, image.shape[:2], i) for (i, vertices) in enumerate(list_of_vertex_lists, start=1))
    if return_all:
        return np.stack(labels)
    else:
        return reduce(np.maximum, labels, np.broadcast_to(0, image.shape[:2]))