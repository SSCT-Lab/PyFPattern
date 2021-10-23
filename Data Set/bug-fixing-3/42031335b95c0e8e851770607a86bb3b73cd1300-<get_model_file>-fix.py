def get_model_file(name, root='~/.mxnet/models/'):
    "Return location for the pretrained on local file system.\n\n    This function will download from online model zoo when model cannot be found or has mismatch.\n    The root directory will be created if it doesn't exist.\n\n    Parameters\n    ----------\n    name : str\n        Name of the model.\n    root : str, default '~/.mxnet/models'\n        Location for keeping the model parameters.\n\n    Returns\n    -------\n    file_path\n        Path to the requested pretrained model file.\n    "
    file_name = '{name}-{short_hash}'.format(name=name, short_hash=short_hash(name))
    root = os.path.expanduser(root)
    file_path = os.path.join(root, (file_name + '.params'))
    sha1_hash = _model_sha1[name]
    if os.path.exists(file_path):
        if check_sha1(file_path, sha1_hash):
            return file_path
        else:
            print('Mismatch in the content of model file detected. Downloading again.')
    else:
        print('Model file is not found. Downloading.')
    if (not os.path.exists(root)):
        os.makedirs(root)
    zip_file_path = os.path.join(root, (file_name + '.zip'))
    repo_url = os.environ.get('MXNET_GLUON_REPO', apache_repo_url)
    if (repo_url[(- 1)] != '/'):
        repo_url = (repo_url + '/')
    download(_url_format.format(repo_url=repo_url, file_name=file_name), path=zip_file_path, overwrite=True)
    with zipfile.ZipFile(zip_file_path) as zf:
        zf.extractall(root)
    os.remove(zip_file_path)
    if check_sha1(file_path, sha1_hash):
        return file_path
    else:
        raise ValueError('Downloaded file has different hash. Please try again.')