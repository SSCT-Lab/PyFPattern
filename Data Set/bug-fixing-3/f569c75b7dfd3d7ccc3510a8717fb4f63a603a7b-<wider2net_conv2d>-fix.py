def wider2net_conv2d(teacher_w1, teacher_b1, teacher_w2, new_width, init):
    "Get initial weights for a wider conv2d layer with a bigger filters,\n    by 'random-padding' or 'net2wider'.\n\n    # Arguments\n        teacher_w1: `weight` of conv2d layer to become wider,\n          of shape (filters1, num_channel1, kh1, kw1)\n        teacher_b1: `bias` of conv2d layer to become wider,\n          of shape (filters1, )\n        teacher_w2: `weight` of next connected conv2d layer,\n          of shape (filters2, num_channel2, kh2, kw2)\n        new_width: new `filters` for the wider conv2d layer\n        init: initialization algorithm for new weights,\n          either 'random-pad' or 'net2wider'\n    "
    assert (teacher_w1.shape[0] == teacher_w2.shape[1]), 'successive layers from teacher model should have compatible shapes'
    assert (teacher_w1.shape[3] == teacher_b1.shape[0]), 'weight and bias from same layer should have compatible shapes'
    assert (new_width > teacher_w1.shape[3]), 'new width (filters) should be bigger than the existing one'
    n = (new_width - teacher_w1.shape[3])
    if (init == 'random-pad'):
        new_w1 = np.random.normal(0, 0.1, size=(teacher_w1.shape[:3] + (n,)))
        new_b1 = (np.ones(n) * 0.1)
        new_w2 = np.random.normal(0, 0.1, size=(teacher_w2.shape[:2] + (n, teacher_w2.shape[3])))
    elif (init == 'net2wider'):
        index = np.random.randint(teacher_w1.shape[3], size=n)
        factors = (np.bincount(index)[index] + 1.0)
        new_w1 = teacher_w1[:, :, :, index]
        new_b1 = teacher_b1[index]
        new_w2 = (teacher_w2[:, :, index, :] / factors.reshape((1, 1, (- 1), 1)))
    else:
        raise ValueError(('Unsupported weight initializer: %s' % init))
    student_w1 = np.concatenate((teacher_w1, new_w1), axis=3)
    if (init == 'random-pad'):
        student_w2 = np.concatenate((teacher_w2, new_w2), axis=2)
    elif (init == 'net2wider'):
        noise = np.random.normal(0, (0.05 * new_w2.std()), size=new_w2.shape)
        student_w2 = np.concatenate((teacher_w2, (new_w2 + noise)), axis=2)
        student_w2[:, :, index, :] = new_w2
    student_b1 = np.concatenate((teacher_b1, new_b1), axis=0)
    return (student_w1, student_b1, student_w2)