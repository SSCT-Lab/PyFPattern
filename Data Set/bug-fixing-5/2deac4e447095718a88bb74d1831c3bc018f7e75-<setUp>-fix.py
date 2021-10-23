def setUp(self):
    self.op_type = 'conv2d'
    self.use_cudnn = False
    self.exhaustive_search = False
    self.use_cuda = False
    self.use_mkldnn = False
    self.data_format = 'AnyLayout'
    self.weighttype = np.float32
    self.use_mkldnn = True
    self.init_group()
    self.init_dilation()
    self.init_test_case()
    self.init_fuse_relu()
    self.init_fuse_residual()
    self.init_data_type()
    conv2d_param = {
        'stride': self.stride,
        'pad': self.pad,
        'dilation': self.dilations,
    }
    filter = np.random.random(self.filter_size).astype(self.weighttype)
    if (self.srctype == np.uint8):
        input = np.random.randint(0, 10, self.input_size).astype(self.srctype)
    else:
        input = np.random.randint((- 5), 5, self.input_size).astype(self.srctype)
        input_shift = (np.ones(self.input_size) * 128).astype(np.uint8)
    if (self.srctype == np.int8):
        filter_int = np.round(((filter * self.scale_weights[0]) * 0.5)).astype(np.int32)
        scale_output_shift = (self.scale_out / ((self.scale_in * self.scale_weights[0]) * 0.5))
        output1 = (conv2d_forward_refer(np.round(((input.astype(np.int32) + input_shift) * self.scale_in)).astype(np.int32), filter_int, self.groups, conv2d_param).astype(np.float32) * scale_output_shift)
        output2 = (conv2d_forward_refer(np.round((input_shift * self.scale_in)).astype(np.int32), filter_int, self.groups, conv2d_param).astype(np.float32) * scale_output_shift)
        if self.fuse_residual:
            input_residual = np.random.randint((- 5), 5, self.input_residual_size).astype(self.srctype)
            output_tmp = np.round(((output1 - output2) + (format_reorder(input_residual, self.input_residual_size).astype(self.srctype) * (self.scale_out / self.scale_in_eltwise))))
            if self.fuse_relu:
                output = np.maximum(output_tmp, 0).astype(self.dsttype)
            else:
                output = output_tmp.astype(self.dsttype)
        elif self.fuse_relu:
            output = np.maximum(np.round((output1 - output2)), 0).astype(self.dsttype)
        else:
            output = np.round((output1 - output2)).astype(self.dsttype)
    else:
        filter_int = np.round((filter * self.scale_weights[0])).astype(np.int32)
        scale_output_shift = (self.scale_out / (self.scale_in * self.scale_weights[0]))
        output1 = conv2d_forward_refer(input.astype(np.int32), filter_int, self.groups, conv2d_param).astype(np.float32)
        output1_tmp = np.round((output1 * (self.scale_out / (self.scale_in * self.scale_weights[0]))))
        if self.fuse_residual:
            input_residual = np.random.randint(0, 10, self.input_residual_size).astype(self.srctype)
            output_tmp_res = np.round(((output1 * (self.scale_out / (self.scale_in * self.scale_weights[0]))) + (format_reorder(input_residual, self.input_residual_size).astype(np.int32) * (self.scale_out / self.scale_in_eltwise))))
            if self.fuse_relu:
                output = np.maximum(output_tmp_res, 0).astype(self.dsttype)
            else:
                output = output_tmp_res.astype(self.dsttype)
        elif self.fuse_relu:
            output = np.maximum(output1_tmp, 0).astype(self.dsttype)
        else:
            output = output1_tmp.astype(self.dsttype)
    self.inputs = {
        'Input': OpTest.np_dtype_to_fluid_dtype(input.astype(self.srctype)),
        'Filter': OpTest.np_dtype_to_fluid_dtype(filter),
    }
    if self.fuse_residual:
        self.inputs['ResidualData'] = OpTest.np_dtype_to_fluid_dtype(input_residual)
    self.attrs = {
        'strides': self.stride,
        'paddings': self.pad,
        'groups': self.groups,
        'dilations': self.dilations,
        'use_cudnn': self.use_cudnn,
        'use_mkldnn': self.use_mkldnn,
        'data_format': self.data_format,
        'exhaustive_search': self.exhaustive_search,
        'Scale_in': self.scale_in,
        'Scale_out': self.scale_out,
        'Scale_weights': self.scale_weights,
        'Scale_in_eltwise': self.scale_in_eltwise,
        'fuse_relu': self.fuse_relu,
        'fuse_residual_connection': self.fuse_residual,
    }
    self.outputs = {
        'Output': output,
    }