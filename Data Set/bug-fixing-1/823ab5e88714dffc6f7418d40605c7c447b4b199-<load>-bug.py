

@templatedoc()
def load(out, file_path, load_as_fp16=None):
    '\n    ${comment}\n\n    >>> import paddle.fluid as fluid\n    >>> tmp_tensor = fluid.layers.create_tensor(dtype=\'float32\')\n    >>> fluid.layers.load(tmp_tensor, "./tmp_tensor.bin")\n\n    Args:\n        out(${out_type}): ${out_comment}.\n\n        file_path(${file_path_type}): ${file_path_comment}.\n\n        load_as_fp16(${load_as_fp16_type}): ${load_as_fp16_comment}.\n\n    Returns:\n        None\n    '
    helper = LayerHelper('load', **locals())
    attrs = {
        'file_path': file_path,
    }
    if (load_as_fp16 is not None):
        attrs['load_as_fp16'] = load_as_fp16
    helper.append_op(type='load', inputs={
        
    }, output={
        'Out': out,
    }, args=attrs)
