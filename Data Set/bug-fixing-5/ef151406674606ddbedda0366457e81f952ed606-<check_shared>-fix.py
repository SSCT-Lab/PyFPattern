def check_shared(axs, x_shared, y_shared):
    '\n    x_shared and y_shared are n x n boolean matrices; entry (i, j) indicates\n    whether the x (or y) axes of subplots i and j should be shared.\n    '
    for ((i1, ax1), (i2, ax2), (i3, (name, shared))) in itertools.product(enumerate(axs), enumerate(axs), enumerate(zip('xy', [x_shared, y_shared]))):
        if (i2 <= i1):
            continue
        assert (getattr(axs[0], '_shared_{}_axes'.format(name)).joined(ax1, ax2) == shared[(i1, i2)]), ('axes %i and %i incorrectly %ssharing %s axis' % (i1, i2, ('not ' if shared[(i1, i2)] else ''), name))