

def _load_info(url=DATA_LIST_URL, encoding='utf-8'):
    'Load dataset information from the network.\n\n    If the network access fails, fall back to a local cache.  This cache gets\n    updated each time a network request _succeeds_.\n    '
    cache_path = os.path.join(BASE_DIR, 'information.json')
    _create_base_dir()
    try:
        info_bytes = urlopen(url).read()
    except (OSError, IOError):
        logger.exception('caught non-fatal exception while trying to update gensim-data cache from %r; using local cache at %r instead', url, cache_path)
    else:
        with open(cache_path, 'wb') as fout:
            fout.write(info_bytes)
    try:
        with io.open(cache_path, 'r', encoding=encoding) as fin:
            return json.load(fin)
    except IOError:
        raise ValueError(('unable to read local cache %r during fallback, connect to the Internet and retry' % cache_path))
