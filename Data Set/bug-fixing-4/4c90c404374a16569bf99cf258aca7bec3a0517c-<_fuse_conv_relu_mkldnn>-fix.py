def _fuse_conv_relu_mkldnn(self, program):
    "\n        Transpile the program by fused relu activation for MKLDNN program.\n        Relu activation following convolution OP can be fused by adding\n        'fuse_relu' attribute to convolution OP.\n        The result of fuse is:\n            - before:\n                - conv->relu->any_other_op\n            - after:\n                - conv->any_other_op\n        :param program: program to transpile\n        :type program: Program\n        "
    self.block = program.block(0)
    i = 0
    while (i < len(self.block.ops)):
        current_op = self.block.ops[i]
        if (current_op.type in ['conv2d']):
            next_op = self.block.ops[(i + 1)]
            if (next_op.type == 'relu'):
                current_op._set_attr('fuse_relu', True)
                self.block._remove_op((i + 1))
        i = (i + 1)
    program = program.clone()