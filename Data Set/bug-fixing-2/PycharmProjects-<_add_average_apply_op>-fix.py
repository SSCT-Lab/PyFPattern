

def _add_average_apply_op(self, block, param_grad):
    param = block._clone_variable(param_grad[0])
    grad = block._clone_variable(param_grad[1])
    sum_1 = block._clone_variable(self._get_accumulator('sum_1', param))
    sum_2 = block._clone_variable(self._get_accumulator('sum_2', param))
    sum_3 = block._clone_variable(self._get_accumulator('sum_3', param))
    num_accumulates = block._clone_variable(self._get_accumulator('num_accumulates', param))
    old_num_accumulates = block._clone_variable(self._get_accumulator('old_num_accumulates', param))
    num_updates = block._clone_variable(self._get_accumulator('num_updates', param))
    layers.assign(input=param, output=grad)
    tmp = layers.sum(x=[num_accumulates, old_num_accumulates])
    sum = layers.sum(x=[sum_1, sum_2, sum_3])
    tmp = layers.cast(x=tmp, dtype=('float32' if (self._dtype == None) else self._dtype))
    sum = layers.cast(x=sum, dtype=('float32' if (self._dtype == None) else self._dtype))
    layers.elementwise_div(x=sum, y=tmp, out=param)
