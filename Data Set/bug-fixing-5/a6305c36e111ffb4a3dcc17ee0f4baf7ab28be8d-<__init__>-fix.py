def __init__(self, config, log):
    super(Itunes, self).__init__(config, log)
    config.add({
        'itunes': {
            'library': '~/Music/iTunes/iTunes Library.xml',
        },
    })
    library_path = config['itunes']['library'].as_filename()
    try:
        self._log.debug('loading iTunes library from {0}'.format(library_path))
        with create_temporary_copy(library_path) as library_copy:
            if six.PY2:
                raw_library = plistlib.readPlist(library_copy)
            else:
                with open(library_copy, 'rb') as library_copy_f:
                    raw_library = plistlib.load(library_copy_f)
    except IOError as e:
        raise ConfigValueError(('invalid iTunes library: ' + e.strerror))
    except Exception:
        if (os.path.splitext(library_path)[1].lower() != '.xml'):
            hint = ': please ensure that the configured path points to the .XML library'
        else:
            hint = ''
        raise ConfigValueError(('invalid iTunes library' + hint))
    self.collection = {_norm_itunes_path(track['Location']): track for track in raw_library['Tracks'].values() if ('Location' in track)}