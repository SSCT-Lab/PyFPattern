

def build(self, input_shape):
    self.input_spec = InputSpec(shape=input_shape)
    if self.stateful:
        self.reset_states()
    else:
        self.states = [None, None]
    if (self.data_format == 'channels_first'):
        channel_axis = 2
    else:
        channel_axis = (- 1)
    if (input_shape[channel_axis] is None):
        raise ValueError('The channel dimension of the inputs should be defined. Found `None`.')
    input_dim = input_shape[channel_axis]
    kernel_shape = (self.kernel_size + (input_dim, (self.filters * 4)))
    self.kernel_shape = kernel_shape
    recurrent_kernel_shape = (self.kernel_size + (self.filters, (self.filters * 4)))
    self.kernel = self.add_weight(kernel_shape, initializer=self.kernel_initializer, name='kernel', regularizer=self.kernel_regularizer, constraint=self.kernel_constraint)
    self.recurrent_kernel = self.add_weight(recurrent_kernel_shape, initializer=self.recurrent_initializer, name='recurrent_kernel', regularizer=self.recurrent_regularizer, constraint=self.recurrent_constraint)
    if self.use_bias:
        self.bias = self.add_weight(((self.filters * 4),), initializer=self.bias_initializer, name='bias', regularizer=self.bias_regularizer, constraint=self.bias_constraint)
        if self.unit_forget_bias:
            bias_value = np.zeros(((self.filters * 4),))
            bias_value[self.filters:(self.filters * 2)] = 1.0
            K.set_value(self.bias, bias_value)
    else:
        self.bias = None
    self.kernel_i = self.kernel[:, :, :, :self.filters]
    self.recurrent_kernel_i = self.recurrent_kernel[:, :, :, :self.filters]
    self.kernel_f = self.kernel[:, :, :, self.filters:(self.filters * 2)]
    self.recurrent_kernel_f = self.recurrent_kernel[:, :, :, self.filters:(self.filters * 2)]
    self.kernel_c = self.kernel[:, :, :, (self.filters * 2):(self.filters * 3)]
    self.recurrent_kernel_c = self.recurrent_kernel[:, :, :, (self.filters * 2):(self.filters * 3)]
    self.kernel_o = self.kernel[:, :, :, (self.filters * 3):]
    self.recurrent_kernel_o = self.recurrent_kernel[:, :, :, (self.filters * 3):]
    if self.use_bias:
        self.bias_i = self.bias[:self.filters]
        self.bias_f = self.bias[self.filters:(self.filters * 2)]
        self.bias_c = self.bias[(self.filters * 2):(self.filters * 3)]
        self.bias_o = self.bias[(self.filters * 3):]
    else:
        self.bias_i = None
        self.bias_f = None
        self.bias_c = None
        self.bias_o = None
    self.built = True
