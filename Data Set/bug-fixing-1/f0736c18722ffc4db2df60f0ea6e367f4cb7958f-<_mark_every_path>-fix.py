

def _mark_every_path(markevery, tpath, affine, ax_transform):
    '\n    Helper function that sorts out how to deal the input\n    `markevery` and returns the points where markers should be drawn.\n\n    Takes in the `markevery` value and the line path and returns the\n    sub-sampled path.\n    '
    (codes, verts) = (tpath.codes, tpath.vertices)

    def _slice_or_none(in_v, slc):
        '\n        Helper function to cope with `codes` being an\n        ndarray or `None`\n        '
        if (in_v is None):
            return None
        return in_v[slc]
    if isinstance(markevery, float):
        markevery = (0.0, markevery)
    elif isinstance(markevery, int):
        markevery = (0, markevery)
    elif isinstance(markevery, np.integer):
        markevery = (0, markevery.item())
    if isinstance(markevery, tuple):
        if (len(markevery) != 2):
            raise ValueError(('`markevery` is a tuple but its len is not 2; markevery=%s' % (markevery,)))
        (start, step) = markevery
        if isinstance(step, int):
            if (not isinstance(start, int)):
                raise ValueError(('`markevery` is a tuple with len 2 and second element is an int, but the first element is not an int; markevery=%s' % (markevery,)))
            return Path(verts[slice(start, None, step)], _slice_or_none(codes, slice(start, None, step)))
        elif isinstance(step, float):
            if (not (isinstance(start, int) or isinstance(start, float))):
                raise ValueError(('`markevery` is a tuple with len 2 and second element is a float, but the first element is not a float or an int; markevery=%s' % (markevery,)))
            disp_coords = affine.transform(tpath.vertices)
            delta = np.empty((len(disp_coords), 2), dtype=float)
            delta[0, :] = 0.0
            delta[1:, :] = (disp_coords[1:, :] - disp_coords[:(- 1), :])
            delta = np.sum((delta ** 2), axis=1)
            delta = np.sqrt(delta)
            delta = np.cumsum(delta)
            scale = ax_transform.transform(np.array([[0, 0], [1, 1]]))
            scale = np.diff(scale, axis=0)
            scale = np.sum((scale ** 2))
            scale = np.sqrt(scale)
            marker_delta = np.arange((start * scale), delta[(- 1)], (step * scale))
            inds = np.abs((delta[np.newaxis, :] - marker_delta[:, np.newaxis]))
            inds = inds.argmin(axis=1)
            inds = np.unique(inds)
            return Path(verts[inds], _slice_or_none(codes, inds))
        else:
            raise ValueError(('`markevery` is a tuple with len 2, but its second element is not an int or a float; markevery=%s' % (markevery,)))
    elif isinstance(markevery, slice):
        return Path(verts[markevery], _slice_or_none(codes, markevery))
    elif iterable(markevery):
        try:
            return Path(verts[markevery], _slice_or_none(codes, markevery))
        except (ValueError, IndexError):
            raise ValueError(('`markevery` is iterable but not a valid form of numpy fancy indexing; markevery=%s' % (markevery,)))
    else:
        raise ValueError(('Value of `markevery` is not recognized; markevery=%s' % (markevery,)))
