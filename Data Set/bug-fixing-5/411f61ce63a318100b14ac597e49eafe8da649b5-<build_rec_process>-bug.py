def build_rec_process(img_dir, train=False, num_thread=1):
    rec_dir = os.path.abspath(os.path.join(img_dir, '../rec'))
    makedirs(rec_dir)
    prefix = ('train' if train else 'val')
    print((('Building ImageRecord file for ' + prefix) + ' ...'))
    to_path = rec_dir
    script_path = os.path.join(rec_dir, 'im2rec.py')
    script_url = 'https://raw.githubusercontent.com/apache/incubator-mxnet/master/tools/im2rec.py'
    download(script_url, script_path)
    lst_path = os.path.join(rec_dir, (prefix + '.lst'))
    lst_url = (('http://data.mxnet.io/models/imagenet/resnet/' + prefix) + '.lst')
    download(lst_url, lst_path)
    cmd = ['python', script_path, rec_dir, img_dir, '--recursive', '--pass-through', '--pack-label', '--num-thread', str(num_thread)]
    subprocess.call(cmd)
    os.remove(script_path)
    os.remove(lst_path)
    print((('ImageRecord file for ' + prefix) + ' has been built!'))