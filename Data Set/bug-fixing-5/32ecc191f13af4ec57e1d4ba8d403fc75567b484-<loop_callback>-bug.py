@staticmethod
def loop_callback(input_type, each):
    assert isinstance(input_type, InputType)
    if (input_type.type == DataType.Dense):
        assert isinstance(each, collections.Sequence)
        for d in each:
            assert isinstance(d, float)
        assert len(each, input_type.dim)
    elif (input_type.type == DataType.Index):
        assert isinstance(each, int)
        assert (each < input_type.dim)
    elif ((input_type.type == DataType.SparseNonValue) or (input_type.type == DataType.SparseValue)):
        assert isinstance(each, collections.Sequence)
        sparse_id = set()
        for k in each:
            if (input_type.type == DataType.SparseValue):
                (k, v) = k
                assert isinstance(v, float)
            assert isinstance(k, int)
            assert (k < input_type.dim)
            sparse_id.add(k)
        assert (len(sparse_id) == len(each))
    else:
        raise RuntimeError('Not support input type')