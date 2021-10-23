def __bfs_travel__(callback, *layers):
    for each_layer in layers:
        __break__ = callback(each_layer)
        if __break__:
            return
        __bfs_travel__(callback, *each_layer.__parent_layers__.values())