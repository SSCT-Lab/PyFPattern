def load_freeimage():
    freeimage = None
    errors = []
    bare_libs = ['FreeImage', 'libfreeimage.dylib', 'libfreeimage.so', 'libfreeimage.so.3']
    (lib_dirs, lib_paths) = _generate_candidate_libs()
    lib_paths = (bare_libs + lib_paths)
    for lib in lib_paths:
        try:
            freeimage = LOADER.LoadLibrary(lib)
            break
        except Exception:
            if (lib not in bare_libs):
                (e_type, e_value, e_tb) = sys.exc_info()
                del e_tb
                errors.append((lib, e_value))
    if (freeimage is None):
        if errors:
            err_txt = [('%s:\n%s' % (l, str(e))) for (l, e) in errors]
            raise RuntimeError('One or more FreeImage libraries were found, but could not be loaded due to the following errors:\n\n\n'.join(err_txt))
        else:
            raise RuntimeError('Could not find a FreeImage library in any of:\n\n'.join(lib_dirs))
    freeimage.FreeImage_SetOutputMessage(c_error_handler)
    return freeimage