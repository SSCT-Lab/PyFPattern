def _number_format(tensor):
    min_sz = 0
    tensor = torch.DoubleTensor(tensor.nelement()).copy_(tensor).abs_()
    pos_inf_mask = tensor.eq(float('inf'))
    neg_inf_mask = tensor.eq(float('-inf'))
    nan_mask = tensor.ne(tensor)
    invalid_value_mask = ((pos_inf_mask + neg_inf_mask) + nan_mask)
    if invalid_value_mask.all():
        tensor = torch.zeros(1)
    example_value = tensor[invalid_value_mask.eq(0)][0]
    tensor[invalid_value_mask] = example_value
    if invalid_value_mask.any():
        min_sz = 3
    int_mode = True
    for value in tensor:
        if (value != math.ceil(value)):
            int_mode = False
            break
    exp_min = tensor.min()
    if (exp_min != 0):
        exp_min = (math.floor(math.log10(exp_min)) + 1)
    else:
        exp_min = 1
    exp_max = tensor.max()
    if (exp_max != 0):
        exp_max = (math.floor(math.log10(exp_max)) + 1)
    else:
        exp_max = 1
    scale = 1
    exp_max = int(exp_max)
    if int_mode:
        if (exp_max > 9):
            format = '{:11.4e}'
            sz = max(min_sz, 11)
        else:
            sz = max(min_sz, (exp_max + 1))
            format = (('{:' + str(sz)) + '.0f}')
    elif ((exp_max - exp_min) > 4):
        sz = 11
        if ((abs(exp_max) > 99) or (abs(exp_min) > 99)):
            sz = (sz + 1)
        sz = max(min_sz, sz)
        format = (('{:' + str(sz)) + '.4e}')
    else:
        if ((exp_max > 5) or (exp_max < 0)):
            sz = max(min_sz, 7)
            scale = math.pow(10, (exp_max - 1))
        else:
            if (exp_max == 0):
                sz = 7
            else:
                sz = (exp_max + 6)
            sz = max(min_sz, sz)
        format = (('{:' + str(sz)) + '.4f}')
    return (format, scale, sz)