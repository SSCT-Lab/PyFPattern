def _InsertQuantOp(context, name, producer, consumers, is_training, moving_avg=True, init_min=(- 6.0), init_max=6.0, bits=8, symmetric=False, ema_decay=0.999, quant_delay=None, vars_collection=ops.GraphKeys.GLOBAL_VARIABLES, narrow_range=False, producer_scope=None, consumer_scope=None):
    'Inserts a quant op between a producer op and (multiple) consumer ops.\n\n  Args:\n    context: Context where producer and consumer operations are nested.\n    name: Name for the new quantization op within the context.\n    producer: Producer operation of the pairs where quantization will be\n      inserted.\n    consumers: Consumer operations of the pairs.\n    is_training: Whether quantizing training graph or eval graph.\n    moving_avg: Specifies whether to use exponential moving average or just\n      the last value seen.\n    init_min: Starting minimum value for the new quantization op.\n    init_max: Starting maximum value for the new quantization op.\n    bits: Number of bits to use for quantization, must be between 2 and 8.\n    symmetric: (Optional) If true, use symmetric quantization limits instead of\n      training the minimum and maximum of each quantization range separately.\n    ema_decay: (Optional) Float, EMA decay parameter.  EMA is used to update\n      quantization intervals for quantizing activations (see here about EMA:\n      https://en.wikipedia.org/wiki/Moving_average#Exponential_moving_average).\n    quant_delay: (Optional, default None) Int, count of global steps for which\n      to delay quantization.  This helps weights stabilize at the start of\n      training.\n    vars_collection: (Optional) Collection where to store the variables for\n      quantization interval ends.\n    narrow_range: Whether to use the narrow quantization range\n      [1; 2^bits - 1] or wide range [0; 2^bits - 1].\n    producer_scope: The restriction of producer scope. If not None, the new op\n      will be inserted only when the producer is in this scope.\n    consumer_scope: The restriction of producer scope. If not None, the new op\n      will be inserted only when all the consumers are in this scope.\n  Raises:\n    ValueError: When producer operation is not directly connected to the\n      consumer operation.\n  '
    if (producer_scope and (not producer.name.startswith(producer_scope))):
        logging.info('_InsertQuantOp ignores context="%s" name="%s" because producer "%s" is not in scope "%s"', context, name, producer.name, producer_scope)
        return
    if consumer_scope:
        consumers_in_scope = []
        for consumer in consumers:
            if consumer.name.startswith(consumer_scope):
                consumers_in_scope.append(consumer)
            else:
                logging.info('_InsertQuantOp context="%s" name="%s" ignores consumer "%s" because it is not in scope "%s"', context, name, consumer.name, consumer_scope)
                return
        consumers = consumers_in_scope
    name_prefix = _AddContextToName(context, name)
    name_scope = ops.get_name_scope()
    if name_scope:
        name_prefix = common.DropStringPrefix(name_prefix, (name_scope + '/'))
    inputs = producer.outputs[0]
    if _FollowedByFakeQuant(inputs):
        return
    if moving_avg:
        quant = quant_ops.MovingAvgQuantize(inputs, init_min=init_min, init_max=init_max, ema_decay=ema_decay, is_training=is_training, num_bits=bits, symmetric=symmetric, narrow_range=narrow_range, vars_collection=vars_collection, name_prefix=name_prefix)
    else:
        quant = quant_ops.LastValueQuantize(inputs, init_min=init_min, init_max=init_max, is_training=is_training, num_bits=bits, symmetric=symmetric, narrow_range=narrow_range, vars_collection=vars_collection, name_prefix=name_prefix)
    if (quant_delay and (quant_delay > 0)):
        activate_quant = math_ops.greater_equal(common.CreateOrGetQuantizationStep(), quant_delay, name=(name_prefix + '/activate_quant'))
        quant = control_flow_ops.cond(activate_quant, (lambda : quant), (lambda : inputs), name=(name_prefix + '/delayed_quant'))
    if consumers:
        tensors_modified_count = common.RerouteTensor(quant, inputs, can_modify=consumers)
        if (tensors_modified_count < len(consumers)):
            raise ValueError(('No inputs quantized for ops: [%s]' % ', '.join([consumer.name for consumer in consumers])))