def find_cudnn_windows_lib():
    proc = Popen(['where', 'cudnn64*.dll'], stdout=PIPE, stderr=PIPE)
    (out, err) = proc.communicate()
    out = out.decode().strip()
    if (len(out) > 0):
        if (out.find('\r\n') != (- 1)):
            out = out.split('\r\n')[0]
        cudnn_lib_name = os.path.basename(out)
        cudnn_lib = os.path.splitext(cudnn_lib_name)[0]
        cudnn_lib = str(cudnn_lib)
        return ctypes.cdll.LoadLibrary(cudnn_lib)
    else:
        return None