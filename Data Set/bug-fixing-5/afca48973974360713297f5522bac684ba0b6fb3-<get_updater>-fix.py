def get_updater(optimizer):
    'Returns a closure of the updater needed for kvstore.\n\n    Parameters\n    ----------\n    optimizer: Optimizer\n         The optimizer.\n\n    Returns\n    -------\n    updater: function\n         The closure of the updater.\n    '
    return Updater(optimizer)