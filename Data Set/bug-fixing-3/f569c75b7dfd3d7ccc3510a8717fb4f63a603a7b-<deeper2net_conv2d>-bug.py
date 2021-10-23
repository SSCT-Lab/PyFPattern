def deeper2net_conv2d(teacher_w):
    "Get initial weights for a deeper conv2d layer by net2deeper'.\n\n    # Arguments\n        teacher_w: `weight` of previous conv2d layer,\n          of shape (filters, num_channel, kh, kw)\n    "
    (filters, num_channel, kh, kw) = teacher_w.shape
    student_w = np.zeros((filters, filters, kh, kw))
    for i in range(filters):
        student_w[(i, i, ((kh - 1) / 2), ((kw - 1) / 2))] = 1.0
    student_b = np.zeros(filters)
    return (student_w, student_b)