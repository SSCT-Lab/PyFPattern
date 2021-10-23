

def scatter(inputs, target_gpus, dim=0):
    '\n    Slices tensors into approximately equal chunks and\n    distributes them across given GPUs. Duplicates\n    references to objects that are not tensors.\n    '

    def scatter_map(obj):
        if isinstance(obj, torch.Tensor):
            return Scatter.apply(target_gpus, None, dim, obj)
        if (isinstance(obj, tuple) and (len(obj) > 0)):
            return list(zip(*map(scatter_map, obj)))
        if (isinstance(obj, list) and (len(obj) > 0)):
            return list(map(list, zip(*map(scatter_map, obj))))
        if (isinstance(obj, dict) and (len(obj) > 0)):
            return list(map(type(obj), zip(*map(scatter_map, obj.items()))))
        return [obj for targets in target_gpus]
    try:
        return scatter_map(inputs)
    finally:
        scatter_map = None
