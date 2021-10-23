def _gather_scales(self, graph):
    for op in graph.all_op_nodes():
        if (op.name() in self._quantize_types):
            bit_length = op.op().attr('bit_length')
            assert (bit_length == 8), 'Unsupported number quantization bits ({}). Only 8 is supported now.'.format(bit_length)
            input_name = op.input('X')[0]
            scale_name = op.input('InScale')[0]
            scale = np.array((1.0 / self._load_param(self._scope, scale_name)[0])).astype(np.float64)
            lod_tensor = self._convert_scale2tensor(scale)
            use_unsigned_int = False
            self._var_quant_scales[input_name] = (use_unsigned_int, lod_tensor)
            self._var_quant_scales[scale_name.replace('.scale', '')] = (use_unsigned_int, lod_tensor)
        if (op.name() in self._fake_dequantize_types):
            input_name = op.input('X')[0]
            _max_range = op.op().attr('max_range')
            self._weight_scales[input_name] = _max_range
    return graph