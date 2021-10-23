

def copyto(dst, src):
    'Copies the elements of an ndarray to those of another one.\n\n    This function can copy the CPU/GPU arrays to the destination arrays on\n    another device.\n\n    Args:\n        dst (`numpy.ndarray`, `cupy.ndarray` or `ideep4py.mdarray`):\n            Destination array.\n        src (`numpy.ndarray`, `cupy.ndarray` or `ideep4py.mdarray`):\n            Source array.\n\n    '
    if isinstance(dst, chainerx.ndarray):
        dst[...] = _chainerx._array_to_chainerx(src, dst.device)
        return
    if isinstance(src, chainerx.ndarray):
        src = from_chx(src)
    if isinstance(dst, numpy.ndarray):
        numpy.copyto(dst, _cpu._to_cpu(src))
    elif isinstance(dst, intel64.mdarray):
        intel64.ideep.basic_copyto(dst, _cpu._to_cpu(src))
    elif isinstance(dst, cuda.ndarray):
        if isinstance(src, chainer.get_cpu_array_types()):
            src = numpy.asarray(src)
            if (dst.flags.c_contiguous or dst.flags.f_contiguous):
                dst.set(src)
            else:
                cuda.cupy.copyto(dst, cuda.to_gpu(src, device=dst.device))
        elif isinstance(src, cuda.ndarray):
            cuda.cupy.copyto(dst, src)
        else:
            raise TypeError('cannot copy from non-array object of type {}'.format(type(src)))
    else:
        raise TypeError('cannot copy to non-array object of type {}'.format(type(dst)))
