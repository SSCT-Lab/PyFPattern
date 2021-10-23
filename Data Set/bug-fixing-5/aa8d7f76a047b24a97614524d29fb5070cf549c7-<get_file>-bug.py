def get_file(fname, origin, untar=False, md5_hash=None, file_hash=None, cache_subdir='datasets', hash_algorithm='auto', extract=False, archive_format='auto', cache_dir=None):
    "Downloads a file from a URL if it not already in the cache.\n\n    By default the file at the url `origin` is downloaded to the\n    cache_dir `~/.keras`, placed in the cache_subdir `datasets`,\n    and given the filename `fname`. The final location of a file\n    `example.txt` would therefore be `~/.keras/datasets/example.txt`.\n\n    Files in tar, tar.gz, tar.bz, and zip formats can also be extracted.\n    Passing a hash will verify the file after download. The command line\n    programs `shasum` and `sha256sum` can compute the hash.\n\n    # Arguments\n        fname: Name of the file. If an absolute path `/path/to/file.txt` is\n            specified the file will be saved at that location.\n        origin: Original URL of the file.\n        untar: Deprecated in favor of 'extract'.\n            boolean, whether the file should be decompressed\n        md5_hash: Deprecated in favor of 'file_hash'.\n            md5 hash of the file for verification\n        file_hash: The expected hash string of the file after download.\n            The sha256 and md5 hash algorithms are both supported.\n        cache_subdir: Subdirectory under the Keras cache dir where the file is\n            saved. If an absolute path `/path/to/folder` is\n            specified the file will be saved at that location.\n        hash_algorithm: Select the hash algorithm to verify the file.\n            options are 'md5', 'sha256', and 'auto'.\n            The default 'auto' detects the hash algorithm in use.\n        extract: True tries extracting the file as an Archive, like tar or zip.\n        archive_format: Archive format to try for extracting the file.\n            Options are 'auto', 'tar', 'zip', and None.\n            'tar' includes tar, tar.gz, and tar.bz files.\n            The default 'auto' is ['tar', 'zip'].\n            None or an empty list will return no matches found.\n        cache_dir: Location to store cached files, when None it\n            defaults to the [Keras Directory](/faq/#where-is-the-keras-configuration-filed-stored).\n\n    # Returns\n        Path to the downloaded file\n    "
    if (cache_dir is None):
        cache_dir = os.path.join(os.path.expanduser('~'), '.keras')
    if ((md5_hash is not None) and (file_hash is None)):
        file_hash = md5_hash
        hash_algorithm = 'md5'
    datadir_base = os.path.expanduser(cache_dir)
    if (not os.access(datadir_base, os.W_OK)):
        datadir_base = os.path.join('/tmp', '.keras')
    datadir = os.path.join(datadir_base, cache_subdir)
    if (not os.path.exists(datadir)):
        os.makedirs(datadir)
    if untar:
        untar_fpath = os.path.join(datadir, fname)
        fpath = (untar_fpath + '.tar.gz')
    else:
        fpath = os.path.join(datadir, fname)
    download = False
    if os.path.exists(fpath):
        if (file_hash is not None):
            if (not validate_file(fpath, file_hash, algorithm=hash_algorithm)):
                print((((('A local file was found, but it seems to be incomplete or outdated because the ' + hash_algorithm) + ' file hash does not match the original value of ') + file_hash) + ' so we will re-download the data.'))
                download = True
    else:
        download = True
    if download:
        print('Downloading data from', origin)

        class ProgressTracker(object):
            progbar = None

        def dl_progress(count, block_size, total_size):
            if (ProgressTracker.progbar is None):
                if (total_size is (- 1)):
                    total_size = None
                ProgressTracker.progbar = Progbar(total_size)
            else:
                ProgressTracker.progbar.update((count * block_size))
        error_msg = 'URL fetch failure on {}: {} -- {}'
        try:
            try:
                urlretrieve(origin, fpath, dl_progress)
            except URLError as e:
                raise Exception(error_msg.format(origin, e.errno, e.reason))
            except HTTPError as e:
                raise Exception(error_msg.format(origin, e.code, e.msg))
        except (Exception, KeyboardInterrupt):
            if os.path.exists(fpath):
                os.remove(fpath)
            raise
        ProgressTracker.progbar = None
    if untar:
        if (not os.path.exists(untar_fpath)):
            _extract_archive(fpath, datadir, archive_format='tar')
        return untar_fpath
    if extract:
        _extract_archive(fpath, datadir, archive_format)
    return fpath