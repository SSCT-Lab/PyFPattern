def meshgrid(*args, **kwargs):
    "Broadcasts parameters for evaluation on an N-D grid.\n\n  Given N one-dimensional coordinate arrays `*args`, returns a list `outputs`\n  of N-D coordinate arrays for evaluating expressions on an N-D grid.\n\n  Notes:\n\n  `meshgrid` supports cartesian ('xy') and matrix ('ij') indexing conventions.\n  When the `indexing` argument is set to 'xy' (the default), the broadcasting\n  instructions for the first two dimensions are swapped.\n\n  Examples:\n\n  Calling `X, Y = meshgrid(x, y)` with the tensors\n\n  ```prettyprint\n    x = [1, 2, 3]\n    y = [4, 5, 6]\n  ```\n\n  results in\n\n  ```prettyprint\n    X = [[1, 1, 1],\n         [2, 2, 2],\n         [3, 3, 3]]\n    Y = [[4, 5, 6],\n         [4, 5, 6],\n         [4, 5, 6]]\n  ```\n\n  Args:\n    *args: `Tensor`s with rank 1\n    indexing: Either 'xy' or 'ij' (optional, default: 'xy')\n    name: A name for the operation (optional).\n\n  Returns:\n    outputs: A list of N `Tensor`s with rank N\n  "
    indexing = kwargs.pop('indexing', 'xy')
    name = kwargs.pop('name', 'meshgrid')
    if kwargs:
        key = list(kwargs.keys())[0]
        raise TypeError("'{}' is an invalid keyword argument for this function".format(key))
    if (indexing not in ('xy', 'ij')):
        raise ValueError("indexing parameter must be either 'xy' or 'ij'")
    with ops.name_scope(name, 'meshgrid', args) as name:
        ndim = len(args)
        s0 = ((1,) * ndim)
        output = []
        for (i, x) in enumerate(args):
            output.append(reshape(stack(x), ((s0[:i] + ((- 1),)) + s0[(i + 1):])))
        shapes = [size(x) for x in args]
        output_dtype = ops.convert_to_tensor(args[0]).dtype.base_dtype
        if ((indexing == 'xy') and (ndim > 1)):
            output[0] = reshape(output[0], ((1, (- 1)) + ((1,) * (ndim - 2))))
            output[1] = reshape(output[1], (((- 1), 1) + ((1,) * (ndim - 2))))
            (shapes[0], shapes[1]) = (shapes[1], shapes[0])
        mult_fact = ones(shapes, output_dtype)
        return [(x * mult_fact) for x in output]