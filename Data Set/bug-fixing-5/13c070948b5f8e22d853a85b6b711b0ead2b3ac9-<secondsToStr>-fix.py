def secondsToStr(t):

    def rediv(ll, b):
        return (list(divmod(ll[0], b)) + ll[1:])
    return ('%d:%02d:%02d.%03d' % tuple(reduce(rediv, [[(t * 1000)], 1000, 60, 60])))