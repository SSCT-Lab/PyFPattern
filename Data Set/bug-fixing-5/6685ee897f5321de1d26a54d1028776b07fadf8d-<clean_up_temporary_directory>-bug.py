def clean_up_temporary_directory():
    for d in _tmpdirs:
        try:
            shutil.rmtree(d)
        except OSError:
            pass