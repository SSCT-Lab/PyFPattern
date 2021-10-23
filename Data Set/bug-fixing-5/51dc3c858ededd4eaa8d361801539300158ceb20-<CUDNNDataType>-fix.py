def CUDNNDataType(name, freefunc=None):
    cargs = []
    if (config.dnn.bin_path and (sys.platform != 'win32')):
        cargs.append(('-Wl,-rpath,' + config.dnn.bin_path))
    return CDataType(name, freefunc, headers=['cudnn.h'], header_dirs=[config.dnn.include_path, config.cuda.include_path], libraries=['cudnn'], lib_dirs=[config.dnn.library_path], compile_args=cargs, version=version(raises=False))