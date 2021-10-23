

def _append_paths_slow(ctx, paths, transforms, clip=None):
    for (path, transform) in zip(paths, transforms):
        for (points, code) in path.iter_segments(transform, remove_nans=True, clip=clip):
            if (code == Path.MOVETO):
                ctx.move_to(*points)
            elif (code == Path.CLOSEPOLY):
                ctx.close_path()
            elif (code == Path.LINETO):
                ctx.line_to(*points)
            elif (code == Path.CURVE3):
                cur = ctx.get_current_point()
                ctx.curve_to(*np.concatenate([((cur / 3) + ((points[:2] * 2) / 3)), (((points[:2] * 2) / 3) + (points[(- 2):] / 3))]))
            elif (code == Path.CURVE4):
                ctx.curve_to(*points)
