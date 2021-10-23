def purge(root=os.path.expanduser('~/.mxnet/models/')):
    "Purge all pretrained model files in local file store.\n\n    Parameters\n    ----------\n    root : str, default '~/.mxnet/models'\n        Location for keeping the model parameters.\n    "
    files = os.listdir(root)
    for f in files:
        if f.endswith('.params'):
            os.remove(os.path.join(root, f))