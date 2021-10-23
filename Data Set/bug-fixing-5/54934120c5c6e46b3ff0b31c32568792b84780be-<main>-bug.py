def main():
    name = 'Market-1501-v15.09.15'
    url = (('http://apache-mxnet.s3-accelerate.dualstack.amazonaws.com/gluon/dataset/' + name) + '.zip')
    root = osp.expanduser('~/.mxnet/datasets')
    if (not os.path.exists(root)):
        os.mkdir(root)
    fpath = osp.join(root, (name + '.zip'))
    exdir = osp.join(root, name)
    if os.path.exists(fpath):
        if (not osp.isdir(exdir)):
            extract(fpath)
            make_list(exdir)
    else:
        download(url, fpath, False)
        extract(fpath)
        make_list(exdir)