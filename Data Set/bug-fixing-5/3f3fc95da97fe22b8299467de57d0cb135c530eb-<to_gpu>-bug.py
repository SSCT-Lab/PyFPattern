def to_gpu(array, device=None, stream=None):
    'Copies the given CPU array to the specified device.\n\n    Args:\n        array: Array to be sent to GPU.\n        device: Device specifier.\n        stream (cupy.cuda.Stream): CUDA stream. If not ``None``, the copy runs\n            asynchronously.\n\n    Returns:\n        cupy.ndarray: Array on GPU.\n\n        If ``array`` is already on the GPU device specified by ``device``,\n        this function just returns ``array`` without performing any copy.\n\n    '
    if (stream is not None):
        warnings.warn('The stream option is deprecated in chainer.cuda.to_gpu. Please remove it.', DeprecationWarning)
    check_cuda_available()
    if (not isinstance(array, (cupy.ndarray, numpy.ndarray))):
        raise TypeError('The array sent to gpu must be numpy.ndarray or cupy.ndarray.\nActual type: {0}.'.format(type(array)))
    with _get_device(device):
        array_dev = get_device_from_array(array)
        if (array_dev.id == cupy.cuda.device.get_device_id()):
            return array
        if ((stream is not None) and (stream.ptr != 0)):
            ret = cupy.empty_like(array)
            if (array_dev.id == (- 1)):
                mem = cupy.cuda.alloc_pinned_memory(array.nbytes)
                src = numpy.frombuffer(mem, array.dtype, array.size).reshape(array.shape)
                src[...] = array
                ret.set(src, stream)
                cupy.cuda.pinned_memory._add_to_watch_list(stream.record(), mem)
            else:
                with array_dev:
                    src = array.copy()
                    event = Stream.null.record()
                stream.wait_event(event)
                ret.data.copy_from_device_async(src.data, src.nbytes, stream)
                stream.add_callback((lambda *x: None), (src, ret))
            return ret
        if (array_dev.id == (- 1)):
            return cupy.asarray(array)
        return cupy.array(array, copy=True)