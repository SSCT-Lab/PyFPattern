def register(reg_name):
    'Register a subclass of CustomOpProp to the registry with name reg_name.'

    def do_register(prop_cls):
        'Register a subclass of CustomOpProp to the registry.'
        fb_functype = CFUNCTYPE(c_bool, c_int, POINTER(c_void_p), POINTER(c_int), POINTER(c_int), c_bool, c_void_p)
        del_functype = CFUNCTYPE(c_bool, c_void_p)

        class CustomOpInfo(Structure):
            'Structure that holds Callback information. Passed to CustomOpProp'
            _fields_ = [('forward', fb_functype), ('backward', fb_functype), ('delete', del_functype), ('p_forward', c_void_p), ('p_backward', c_void_p), ('p_delete', c_void_p)]
        infer_functype = CFUNCTYPE(c_bool, c_int, POINTER(c_int), POINTER(POINTER(mx_uint)), c_void_p)
        list_functype = CFUNCTYPE(c_bool, POINTER(POINTER(POINTER(c_char))), c_void_p)
        deps_functype = CFUNCTYPE(c_bool, c_int_p, c_int_p, c_int_p, c_int_p, POINTER(c_int_p), c_void_p)
        createop_functype = CFUNCTYPE(c_bool, c_char_p, c_int, POINTER(POINTER(mx_uint)), POINTER(c_int), POINTER(c_int), POINTER(CustomOpInfo), c_void_p)

        class CustomOpPropInfo(Structure):
            'Structure that holds Callback information. Passed to CustomOpProp'
            _fields_ = [('list_arguments', list_functype), ('list_outputs', list_functype), ('infer_shape', infer_functype), ('declare_backward_dependency', deps_functype), ('create_operator', createop_functype), ('list_auxiliary_states', list_functype), ('delete', del_functype), ('p_list_arguments', c_void_p), ('p_list_outputs', c_void_p), ('p_infer_shape', c_void_p), ('p_declare_backward_dependency', c_void_p), ('p_create_operator', c_void_p), ('p_list_auxiliary_states', c_void_p), ('p_delete', c_void_p)]
        req_enum = ['null', 'write', 'inplace', 'add']

        def creator(op_type, argc, keys, vals, ret):
            'internal function'
            assert (py_str(op_type) == reg_name)
            kwargs = dict([(py_str(keys[i]), py_str(vals[i])) for i in range(argc)])
            op_prop = prop_cls(**kwargs)

            def infer_shape_entry(num_tensor, tensor_dims, tensor_shapes, _):
                'C Callback for CustomOpProp::InferShape'
                try:
                    n_in = len(op_prop.list_arguments())
                    n_out = len(op_prop.list_outputs())
                    n_aux = len(op_prop.list_auxiliary_states())
                    assert (num_tensor == ((n_in + n_out) + n_aux))
                    shapes = [[tensor_shapes[i][j] for j in range(tensor_dims[i])] for i in range(n_in)]
                    ret = op_prop.infer_shape(shapes)
                    if (len(ret) == 2):
                        (ishape, oshape) = ret
                        ashape = []
                    elif (len(ret) == 3):
                        (ishape, oshape, ashape) = ret
                    else:
                        raise AssertionError('infer_shape must return 2 or 3 lists')
                    assert (len(oshape) == n_out)
                    assert (len(ishape) == n_in)
                    assert (len(ashape) == n_aux)
                    rshape = ((list(ishape) + list(oshape)) + list(ashape))
                    for i in range(((n_in + n_out) + n_aux)):
                        tensor_shapes[i] = cast(c_array(mx_uint, rshape[i]), POINTER(mx_uint))
                        tensor_dims[i] = len(rshape[i])
                    infer_shape_entry._ref_holder = [tensor_shapes]
                except Exception as e:
                    print(('Error in %s.infer_shape: ' % reg_name), str(e))
                    return False
                return True

            def list_outputs_entry(out, _):
                'C Callback for CustomOpProp::ListOutputs'
                try:
                    ret = op_prop.list_outputs()
                    ret = ([c_str(i) for i in ret] + [c_char_p(0)])
                    ret = c_array(c_char_p, ret)
                    out[0] = cast(ret, POINTER(POINTER(c_char)))
                    list_outputs_entry._ref_holder = [out]
                except Exception as e:
                    print(('Error in %s.list_outputs: ' % reg_name), str(e))
                    return False
                return True

            def list_arguments_entry(out, _):
                'C Callback for CustomOpProp::ListArguments'
                try:
                    ret = op_prop.list_arguments()
                    ret = ([c_str(i) for i in ret] + [c_char_p(0)])
                    ret = c_array(c_char_p, ret)
                    out[0] = cast(ret, POINTER(POINTER(c_char)))
                    list_arguments_entry._ref_holder = [out]
                except Exception as e:
                    print(('Error in %s.list_arguments: ' % reg_name), str(e))
                    return False
                return True

            def list_auxiliary_states_entry(out, _):
                'C Callback for CustomOpProp::ListAuxiliaryStates'
                try:
                    ret = op_prop.list_auxiliary_states()
                    ret = ([c_str(i) for i in ret] + [c_char_p(0)])
                    ret = c_array(c_char_p, ret)
                    out[0] = cast(ret, POINTER(POINTER(c_char)))
                    list_auxiliary_states_entry._ref_holder = [out]
                except Exception as e:
                    print(('Error in %s.list_auxiliary_states: ' % reg_name), str(e))
                    return False
                return True

            def declare_backward_dependency_entry(out_grad, in_data, out_data, num_dep, deps, _):
                'C Callback for CustomOpProp::DeclareBacwardDependency'
                try:
                    out_grad = [out_grad[i] for i in range(len(op_prop.list_outputs()))]
                    in_data = [in_data[i] for i in range(len(op_prop.list_arguments()))]
                    out_data = [out_data[i] for i in range(len(op_prop.list_outputs()))]
                    rdeps = op_prop.declare_backward_dependency(out_grad, in_data, out_data)
                    num_dep[0] = len(rdeps)
                    rdeps = cast(c_array(c_int, rdeps), c_int_p)
                    deps[0] = rdeps
                    declare_backward_dependency_entry._ref_holder = [deps]
                except Exception as e:
                    print(('Error in %s.declare_backward_dependency: ' % reg_name), str(e))
                    return False
                return True

            def create_operator_entry(ctx, num_inputs, shapes, ndims, dtypes, ret, _):
                'C Callback for CustomOpProp::CreateOperator'
                try:
                    ndims = [ndims[i] for i in range(num_inputs)]
                    shapes = [[shapes[i][j] for j in range(ndims[i])] for i in range(num_inputs)]
                    dtypes = [dtypes[i] for i in range(num_inputs)]
                    op = op_prop.create_operator(ctx, shapes, dtypes)

                    def forward_entry(num_ndarray, ndarraies, tags, reqs, is_train, _):
                        'C Callback for CustomOp::Forward'
                        try:
                            tensors = [[] for i in range(5)]
                            for i in range(num_ndarray):
                                if ((tags[i] == 1) or (tags[i] == 4)):
                                    tensors[tags[i]].append(NDArray(cast(ndarraies[i], NDArrayHandle), writable=True))
                                else:
                                    tensors[tags[i]].append(NDArray(cast(ndarraies[i], NDArrayHandle), writable=False))
                            reqs = [req_enum[reqs[i]] for i in range(len(tensors[1]))]
                            op.forward(is_train=is_train, req=reqs, in_data=tensors[0], out_data=tensors[1], aux=tensors[4])
                        except Exception as e:
                            print('Error in CustomOp.forward: ', str(e))
                            return False
                        return True

                    def backward_entry(num_ndarray, ndarraies, tags, reqs, is_train, _):
                        'C Callback for CustomOp::Backward'
                        try:
                            tensors = [[] for i in range(5)]
                            for i in range(num_ndarray):
                                if ((tags[i] == 2) or (tags[i] == 4)):
                                    tensors[tags[i]].append(NDArray(cast(ndarraies[i], NDArrayHandle), writable=True))
                                else:
                                    tensors[tags[i]].append(NDArray(cast(ndarraies[i], NDArrayHandle), writable=False))
                            reqs = [req_enum[reqs[i]] for i in range(len(tensors[2]))]
                            op.backward(req=reqs, in_data=tensors[0], out_data=tensors[1], in_grad=tensors[2], out_grad=tensors[3], aux=tensors[4])
                        except Exception as e:
                            print('Error in CustomOp.backward: ', str(e))
                            return False
                        return True
                    cur = _registry.inc()

                    def delete_entry(_):
                        'C Callback for CustomOp::del'
                        try:
                            del _registry.ref_holder[cur]
                        except Exception as e:
                            print('Error in CustomOp.delete: ', str(e))
                            return False
                        return True
                    ret[0] = CustomOpInfo(fb_functype(forward_entry), fb_functype(backward_entry), del_functype(delete_entry), None, None, None)
                    op._ref_holder = [ret]
                    _registry.ref_holder[cur] = op
                except Exception as e:
                    print(('Error in %s.create_operator: ' % reg_name), str(e))
                    return False
                return True
            cur = _registry.inc()

            def delete_entry(_):
                'C Callback for CustomOpProp::del'
                try:
                    del _registry.ref_holder[cur]
                except Exception as e:
                    print('Error in CustomOpProp.delete: ', str(e))
                    return False
                return True
            ret[0] = CustomOpPropInfo(list_functype(list_arguments_entry), list_functype(list_outputs_entry), infer_functype(infer_shape_entry), deps_functype(declare_backward_dependency_entry), createop_functype(create_operator_entry), list_functype(list_auxiliary_states_entry), del_functype(delete_entry), None, None, None, None, None, None, None)
            op_prop._ref_holder = [ret]
            _registry.ref_holder[cur] = op_prop
            return True
        creator_functype = CFUNCTYPE(c_bool, c_char_p, c_int, POINTER(c_char_p), POINTER(c_char_p), POINTER(CustomOpPropInfo))
        creator_func = creator_functype(creator)
        check_call(_LIB.MXCustomOpRegister(c_str(reg_name), creator_func))
        cur = _registry.inc()
        _registry.ref_holder[cur] = creator_func
        return prop_cls
    return do_register