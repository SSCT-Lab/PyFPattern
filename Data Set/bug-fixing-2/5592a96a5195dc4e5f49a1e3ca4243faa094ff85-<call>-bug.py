

def call(self, inputs, training=None):
    if (training is None):
        training = K.learning_phase()
    in_eager_mode = context.executing_eagerly()
    if (self.virtual_batch_size is not None):
        original_shape = ([(- 1)] + inputs.shape.as_list()[1:])
        expanded_shape = ([self.virtual_batch_size, (- 1)] + original_shape[1:])
        inputs = array_ops.reshape(inputs, expanded_shape)

        def undo_virtual_batching(outputs):
            outputs = array_ops.reshape(outputs, original_shape)
            return outputs
    if self.fused:
        outputs = self._fused_batch_norm(inputs, training=training)
        if (self.virtual_batch_size is not None):
            outputs = undo_virtual_batching(outputs)
        if ((not context.executing_eagerly()) and (training is K.learning_phase())):
            outputs._uses_learning_phase = True
        return outputs
    input_shape = inputs.get_shape()
    ndims = len(input_shape)
    reduction_axes = [i for i in range(ndims) if (i not in self.axis)]
    if (self.virtual_batch_size is not None):
        del reduction_axes[1]
    broadcast_shape = ([1] * ndims)
    broadcast_shape[self.axis[0]] = input_shape[self.axis[0]].value

    def _broadcast(v):
        if ((v is not None) and (len(v.get_shape()) != ndims) and (reduction_axes != list(range((ndims - 1))))):
            return array_ops.reshape(v, broadcast_shape)
        return v
    (scale, offset) = (_broadcast(self.gamma), _broadcast(self.beta))

    def _compose_transforms(scale, offset, then_scale, then_offset):
        if (then_scale is not None):
            scale *= then_scale
            offset *= then_scale
        if (then_offset is not None):
            offset += then_offset
        return (scale, offset)
    training_value = tf_utils.constant_value(training)
    if (training_value is not False):
        if self.adjustment:
            (adj_scale, adj_bias) = self.adjustment(array_ops.shape(inputs))
            adj_scale = tf_utils.smart_cond(training, (lambda : adj_scale), (lambda : array_ops.ones_like(adj_scale)))
            adj_bias = tf_utils.smart_cond(training, (lambda : adj_bias), (lambda : array_ops.zeros_like(adj_bias)))
            (scale, offset) = _compose_transforms(adj_scale, adj_bias, scale, offset)
        keep_dims = ((self.virtual_batch_size is not None) or (len(self.axis) > 1))
        (mean, variance) = nn.moments(inputs, reduction_axes, keep_dims=keep_dims)
        moving_mean = self.moving_mean
        moving_variance = self.moving_variance
        mean = tf_utils.smart_cond(training, (lambda : mean), (lambda : moving_mean))
        variance = tf_utils.smart_cond(training, (lambda : variance), (lambda : moving_variance))
        if self.renorm:
            (r, d, new_mean, new_variance) = self._renorm_correction_and_moments(mean, variance, training)
            r = _broadcast(array_ops.stop_gradient(r, name='renorm_r'))
            d = _broadcast(array_ops.stop_gradient(d, name='renorm_d'))
            (scale, offset) = _compose_transforms(r, d, scale, offset)
        else:
            (new_mean, new_variance) = (mean, variance)
        if (self.virtual_batch_size is not None):
            new_mean = math_ops.reduce_mean(new_mean, axis=1, keep_dims=True)
            new_variance = math_ops.reduce_mean(new_variance, axis=1, keep_dims=True)

        def _do_update(var, value):
            if (in_eager_mode and (not self.trainable)):
                return
            return self._assign_moving_average(var, value, self.momentum)
        mean_update = tf_utils.smart_cond(training, (lambda : _do_update(self.moving_mean, new_mean)), (lambda : self.moving_mean))
        variance_update = tf_utils.smart_cond(training, (lambda : _do_update(self.moving_variance, new_variance)), (lambda : self.moving_variance))
        if (not context.executing_eagerly()):
            self.add_update(mean_update, inputs=True)
            self.add_update(variance_update, inputs=True)
    else:
        (mean, variance) = (self.moving_mean, self.moving_variance)
    outputs = nn.batch_normalization(inputs, _broadcast(mean), _broadcast(variance), offset, scale, self.epsilon)
    outputs.set_shape(input_shape)
    if (self.virtual_batch_size is not None):
        outputs = undo_virtual_batching(outputs)
    if ((not context.executing_eagerly()) and (training is K.learning_phase())):
        outputs._uses_learning_phase = True
    return outputs
