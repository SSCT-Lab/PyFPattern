def maybe_download_and_extract():
    "Download and extract model tar file.\n\n  If the pretrained model we're using doesn't already exist, this function\n  downloads it from the TensorFlow.org website and unpacks it into a directory.\n  "
    dest_directory = FLAGS.model_dir
    if (not os.path.exists(dest_directory)):
        os.makedirs(dest_directory)
    filename = DATA_URL.split('/')[(- 1)]
    filepath = os.path.join(dest_directory, filename)
    if (not os.path.exists(filepath)):

        def _progress(count, block_size, total_size):
            sys.stdout.write(('\r>> Downloading %s %.1f%%' % (filename, ((float((count * block_size)) / float(total_size)) * 100.0))))
            sys.stdout.flush()
        (filepath, _) = urllib.request.urlretrieve(DATA_URL, filepath, _progress)
        print()
        statinfo = os.stat(filepath)
        print('Successfully downloaded', filename, statinfo.st_size, 'bytes.')
    tarfile.open(filepath, 'r:gz').extractall(dest_directory)