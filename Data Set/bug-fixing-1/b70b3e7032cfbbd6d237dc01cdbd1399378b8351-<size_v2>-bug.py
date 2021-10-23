

@tf_export('size', v1=[])
@dispatch.add_dispatch_support
def size_v2(input, out_type=dtypes.int32, name=None):
    return size(input, name, out_type)
