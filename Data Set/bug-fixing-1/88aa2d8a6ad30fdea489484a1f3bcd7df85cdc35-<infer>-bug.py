

def infer(use_cuda, inference_program, params_dirname):
    place = (fluid.CUDAPlace(0) if use_cuda else fluid.CPUPlace())
    inferencer = fluid.Inferencer(inference_program, param_path=params_dirname, place=place)
    lod = [[3, 4, 2]]
    base_shape = [1]
    word = fluid.create_random_int_lodtensor(lod, base_shape, place, low=0, high=(WORD_DICT_LEN - 1))
    pred = fluid.create_random_int_lodtensor(lod, base_shape, place, low=0, high=(PRED_DICT_LEN - 1))
    ctx_n2 = fluid.create_random_int_lodtensor(lod, base_shape, place, low=0, high=(WORD_DICT_LEN - 1))
    ctx_n1 = fluid.create_random_int_lodtensor(lod, base_shape, place, low=0, high=(WORD_DICT_LEN - 1))
    ctx_0 = fluid.create_random_int_lodtensor(lod, base_shape, place, low=0, high=(WORD_DICT_LEN - 1))
    ctx_p1 = fluid.create_random_int_lodtensor(lod, base_shape, place, low=0, high=(WORD_DICT_LEN - 1))
    ctx_p2 = fluid.create_random_int_lodtensor(lod, base_shape, place, low=0, high=(WORD_DICT_LEN - 1))
    mark = fluid.create_random_int_lodtensor(lod, base_shape, place, low=0, high=(MARK_DICT_LEN - 1))
    results = inferencer.infer({
        'word_data': word,
        'verb_data': pred,
        'ctx_n2_data': ctx_n2,
        'ctx_n1_data': ctx_n1,
        'ctx_0_data': ctx_0,
        'ctx_p1_data': ctx_p1,
        'ctx_p2_data': ctx_p2,
        'mark_data': mark,
    }, return_numpy=False)
    print('infer results: ', np.array(results[0]))
