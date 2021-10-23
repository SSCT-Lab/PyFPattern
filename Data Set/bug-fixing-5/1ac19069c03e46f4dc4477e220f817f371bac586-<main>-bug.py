def main(sdl2=False):
    machine_type = get_machine_type()
    prebuilt_dir = ('prebuilt-%s' % machine_type)
    use_prebuilt = ('-prebuilt' in sys.argv)
    auto_download = ('PYGAME_DOWNLOAD_PREBUILT' in os.environ)
    if auto_download:
        auto_download = (os.environ['PYGAME_DOWNLOAD_PREBUILT'] == '1')
    try:
        from . import download_win_prebuilt
    except ImportError:
        import download_win_prebuilt
    download_kwargs = {
        'x86': False,
        'x64': False,
        'sdl2': sdl2,
    }
    download_kwargs[machine_type] = True
    if (not auto_download):
        if (((not download_win_prebuilt.cached(**download_kwargs)) or (not os.path.isdir(prebuilt_dir))) and download_win_prebuilt.ask(**download_kwargs)):
            use_prebuilt = True
    else:
        download_win_prebuilt.update(**download_kwargs)
    if os.path.isdir(prebuilt_dir):
        if (not use_prebuilt):
            if ('PYGAME_USE_PREBUILT' in os.environ):
                use_prebuilt = (os.environ['PYGAME_USE_PREBUILT'] == '1')
            else:
                logging.warning(('Using the SDL libraries in "%s".' % prebuilt_dir))
                use_prebuilt = True
        if use_prebuilt:
            if sdl2:
                return setup_prebuilt_sdl2(prebuilt_dir)
            setup_prebuilt_sdl1(prebuilt_dir)
            raise SystemExit()
    else:
        print(('Note: cannot find directory "%s"; do not use prebuilts.' % prebuilt_dir))
    return setup(sdl2)