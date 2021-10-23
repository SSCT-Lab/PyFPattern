def deeper2net_conv2d(teacher_w):
    "Get initial weights for a deeper conv2d layer by net2deeper'.\n\n    # Arguments\n        teacher_w: `weight` of previous conv2d layer,\n          of shape (kh, kw, num_channel, filters)\n    "
    (kh, kw, num_channel, filters) = teacher_w.shape
    student_w = np.zeros_like(teacher_w)
    for i in range(filters):
        student_w[(((kh - 1) / 2), ((kw - 1) / 2), i, i)] = 1.0
    student_b = np.zeros(filters)
    return (student_w, student_b)