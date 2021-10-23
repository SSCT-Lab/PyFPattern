def load_url(url, model_dir=None, map_location=None):
    "Loads the Torch serialized object at the given URL.\n\n    If the object is already present in `model_dir`, it's deserialied and\n    returned. The filename part of the URL should follow the naming convention\n    ``filename-<sha256>.ext`` where ``<sha256>`` is the first eight or more\n    digits of the SHA256 hash of the contents of the file. The hash is used to\n    ensure unique names and to verify the contents of the file.\n\n    The default value of `model_dir` is ``$TORCH_HOME/models`` where\n    ``$TORCH_HOME`` defaults to ``~/.torch``. The default directory can be\n    overriden with the ``$TORCH_MODEL_ZOO`` environement variable.\n\n    Args:\n        url (string): URL of the object to download\n        model_dir (string, optional): directory in which to save the object\n        map_location (optional): a function or a dict specifying how to remap storage locations (see torch.load)\n\n    Example:\n        >>> state_dict = torch.utils.model_zoo.load_url('https://s3.amazonaws.com/pytorch/models/resnet18-5c106cde.pth')\n\n    "
    if (model_dir is None):
        torch_home = os.path.expanduser(os.getenv('TORCH_HOME', '~/.torch'))
        model_dir = os.getenv('TORCH_MODEL_ZOO', os.path.join(torch_home, 'models'))
    if (not os.path.exists(model_dir)):
        os.makedirs(model_dir)
    parts = urlparse(url)
    filename = os.path.basename(parts.path)
    cached_file = os.path.join(model_dir, filename)
    if (not os.path.exists(cached_file)):
        sys.stderr.write('Downloading: "{}" to {}\n'.format(url, cached_file))
        hash_prefix = HASH_REGEX.search(filename).group(1)
        _download_url_to_file(url, cached_file, hash_prefix)
    return torch.load(cached_file, map_location=map_location)