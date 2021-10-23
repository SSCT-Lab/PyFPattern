

def _find_lib_path():
    'Find mxnet library.'
    curr_path = os.path.dirname(os.path.abspath(os.path.expanduser(__file__)))
    amalgamation_lib_path = os.path.join(curr_path, '../../lib/libmxnet_predict.so')
    if (os.path.exists(amalgamation_lib_path) and os.path.isfile(amalgamation_lib_path)):
        lib_path = [amalgamation_lib_path]
        return lib_path
    else:
        logging.info('Cannot find libmxnet_predict.so. Will search for MXNet library using libinfo.py then.')
        try:
            from mxnet.libinfo import find_lib_path
            lib_path = find_lib_path()
            return lib_path
        except ImportError:
            libinfo_path = os.path.join(curr_path, '../../python/mxnet/libinfo.py')
            if (os.path.exists(libinfo_path) and os.path.isfile(libinfo_path)):
                libinfo = {
                    '__file__': libinfo_py,
                }
                exec(compile(open(libinfo_py, 'rb').read(), libinfo_py, 'exec'), libinfo, libinfo)
                lib_path = libinfo['find_lib_path']()
                return lib_path
            else:
                raise RuntimeError(('Cannot find libinfo.py at %s.' % libinfo_path))
