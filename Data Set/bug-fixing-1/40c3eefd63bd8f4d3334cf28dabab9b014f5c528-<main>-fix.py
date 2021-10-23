

def main():
    args = parse_args()
    target_dir = os.path.expanduser(args.target_dir)
    if os.path.exists(target_dir):
        raise ValueError((('Target dir [' + target_dir) + '] exists. Remove it first'))
    tar_dir = os.path.expanduser(args.target_dir)
    download_dir = os.path.expanduser(args.download_dir)
    train_tar_fname = os.path.join(download_dir, _TRAIN_TAR)
    check_file(train_tar_fname, args.checksum, _TRAIN_TAR_SHA1)
    val_tar_fname = os.path.join(download_dir, _VAL_TAR)
    check_file(val_tar_fname, args.checksum, _VAL_TAR_SHA1)
    extract_train(train_tar_fname, os.path.join(target_dir, 'train'))
    extract_val(val_tar_fname, os.path.join(target_dir, 'val'))
