def clean_up_temporary_directory():
    if (_tmpdirs is not None):
        for d in _tmpdirs:
            try:
                shutil.rmtree(d)
            except OSError:
                pass