def _fuse_conv_eltwise(self, conv_op, eltwise_op):
    '\n        fuse the conv op with elementwise_add\n\n        :param conv_op: convolution operator\n        :type conv_op: Operator\n        :param eltwise_op: operator adding data from skip connection\n        :type eltwise_op: Operator\n        '
    conv_op.set_attr('fuse_eltwise', True)
    self.input_map[conv_op.output('Output')[0]] = eltwise_op.input('Y')[0]
    self.input_map[eltwise_op.output('Out')[0]] = eltwise_op.input('Y')[0]