def get_device(device_spec):
    "Returns a device object.\n\n    Args:\n        device_spec (object): Device specifier.\n            If a :class:`chainer.backend.Device` instance is given, it is\n            returned intact. Otherwise the following values are supported:\n\n            * ChainerX devices\n\n              * A string representing a device.\n                (ex. ``'native:0'``, ``'native'``)\n              * A :class:`chainerx.Device` object.\n\n            * CuPy\n\n              * A string starts with ``'@cupy:'``.\n                (ex. ``'@cupy:0'``)\n              * A :class:`cupy.cuda.Device` object.\n\n            * NumPy\n\n              * The string ``'@numpy'``.\n\n            * NumPy with Intel Architecture\n\n              * The string ``'@intel64'``.\n    "
    if isinstance(device_spec, Device):
        return device_spec
    if isinstance(device_spec, cuda._integer_types):
        return _get_device_cupy_or_numpy(device_spec)
    if (chainerx.is_available() and isinstance(device_spec, chainerx.Device)):
        return _chainerx.ChainerxDevice(device_spec)
    if (cuda.available and isinstance(device_spec, cuda.Device)):
        return cuda.GpuDevice(device_spec)
    if isinstance(device_spec, six.string_types):
        try:
            int_device_spec = int(device_spec)
        except ValueError:
            pass
        else:
            return _get_device_cupy_or_numpy(int_device_spec)
        if device_spec.startswith('@'):
            (mod_name, colon, precise_spec) = device_spec[1:].partition(':')
            if (mod_name == 'numpy'):
                if (not colon):
                    return _cpu.CpuDevice()
            elif (mod_name == 'cupy'):
                if colon:
                    return cuda.GpuDevice.from_device_id(int(precise_spec))
            elif (mod_name == 'intel64'):
                if (not colon):
                    return intel64.Intel64Device()
            raise ValueError("Device specifiers starting with '@' must be followed by a module name and depending on the module, module specific precise device specifiers. Actual: {}".format(device_spec))
        else:
            if (not chainerx.is_available()):
                raise RuntimeError("Tried to parse ChainerX device specifier '{}', but ChainerX is not available. Note that device specifiers without '@' prefix are assumed to be ChainerX device specifiers.".format(device_spec))
            return _chainerx.ChainerxDevice(chainerx.get_device(device_spec))
    raise TypeError('Device specifier must be a backend.Device, cuda.Device, chainerx.Device, integer or a string. Actual: {}'.format(type(device_spec)))