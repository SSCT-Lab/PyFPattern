@contextlib.contextmanager
def time_range(message, color_id=None, argb_color=None):
    "A context manager to describe the enclosed block as a nested range\n\n    >>> with cupy.prof.time_range('some range in green', color_id=0):\n    ...    # do something you want to measure\n    ...    pass\n\n    Args:\n        message: Name of a range.\n        color_id: range color ID\n        argb_color: range color in ARGB (e.g. 0xFF00FF00 for green)\n\n    .. seealso:: :func:`cupy.cuda.nvtx.RangePush`\n        :func:`cupy.cuda.nvtx.RangePop`\n    "
    if ((color_id is not None) and (argb_color is not None)):
        raise ValueError('Only either color_id or argb_color can be specified')
    if (argb_color is not None):
        nvtx.RangePushC(message, argb_color)
    else:
        if (color_id is None):
            color_id = (- 1)
        nvtx.RangePush(message, color_id)
    try:
        (yield)
    finally:
        nvtx.RangePop()