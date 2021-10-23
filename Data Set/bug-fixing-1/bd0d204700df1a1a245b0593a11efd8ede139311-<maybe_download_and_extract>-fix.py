

def maybe_download_and_extract(data_url):
    "Download and extract model tar file.\n\n  If the pretrained model we're using doesn't already exist, this function\n  downloads it from the TensorFlow.org website and unpacks it into a directory.\n\n  Args:\n    data_url: Web location of the tar file containing the pretrained model.\n  "
    dest_directory = FLAGS.model_dir
    if (not os.path.exists(dest_directory)):
        os.makedirs(dest_directory)
    filename = data_url.split('/')[(- 1)]
    filepath = os.path.join(dest_directory, filename)
    if (not os.path.exists(filepath)):

        def _progress(count, block_size, total_size):
            sys.stdout.write(('\r>> Downloading %s %.1f%%' % (filename, ((float((count * block_size)) / float(total_size)) * 100.0))))
            sys.stdout.flush()
        (filepath, _) = urllib.request.urlretrieve(data_url, filepath, _progress)
        print()
        statinfo = os.stat(filepath)
        tf.logging.info('Successfully downloaded %s %d bytes.', filename, statinfo.st_size)
        print('Extracting file from ', filepath)
        tarfile.open(filepath, 'r:gz').extractall(dest_directory)
    else:
        print('Not extracting or downloading files, model already present in disk')
