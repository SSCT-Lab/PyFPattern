

def _download(name):
    'Download and extract the dataset/model.\n\n    Parameters\n    ----------\n    name: str\n        Dataset/model name which has to be downloaded.\n\n    Raises\n    ------\n    Exception\n        If md5sum on client and in repo are different.\n\n    '
    url_load_file = '{base}/{fname}/__init__.py'.format(base=DOWNLOAD_BASE_URL, fname=name)
    data_folder_dir = os.path.join(base_dir, name)
    data_folder_dir_tmp = (data_folder_dir + '_tmp')
    tmp_dir = tempfile.mkdtemp()
    init_path = os.path.join(tmp_dir, '__init__.py')
    urllib.urlretrieve(url_load_file, init_path)
    total_parts = _get_parts(name)
    if (total_parts > 1):
        concatenated_folder_name = '{fname}.gz'.format(fname=name)
        concatenated_folder_dir = os.path.join(tmp_dir, concatenated_folder_name)
        for part in range(0, total_parts):
            url_data = '{base}/{fname}/{fname}.gz_0{part}'.format(base=DOWNLOAD_BASE_URL, fname=name, part=part)
            fname = '{f}.gz_0{p}'.format(f=name, p=part)
            dst_path = os.path.join(tmp_dir, fname)
            urllib.urlretrieve(url_data, dst_path, reporthook=partial(_progress, part=part, total_parts=total_parts))
            if (_calculate_md5_checksum(dst_path) == _get_checksum(name, part)):
                sys.stdout.write('\n')
                sys.stdout.flush()
                logger.info('Part %s/%s downloaded', (part + 1), total_parts)
            else:
                shutil.rmtree(tmp_dir)
                raise Exception('Checksum comparison failed, try again')
        with open(concatenated_folder_dir, 'wb') as wfp:
            for part in range(0, total_parts):
                part_path = os.path.join(tmp_dir, '{fname}.gz_0{part}'.format(fname=name, part=part))
                with open(part_path, 'rb') as rfp:
                    shutil.copyfileobj(rfp, wfp)
                os.remove(part_path)
    else:
        url_data = '{base}/{fname}/{fname}.gz'.format(base=DOWNLOAD_BASE_URL, fname=name)
        fname = '{fname}.gz'.format(fname=name)
        dst_path = os.path.join(tmp_dir, fname)
        urllib.urlretrieve(url_data, dst_path, reporthook=_progress)
        if (_calculate_md5_checksum(dst_path) == _get_checksum(name)):
            sys.stdout.write('\n')
            sys.stdout.flush()
            logger.info('%s downloaded', name)
        else:
            shutil.rmtree(tmp_dir)
            raise Exception('Checksum comparison failed, try again')
    if os.path.exists(data_folder_dir_tmp):
        os.remove(data_folder_dir_tmp)
    shutil.move(tmp_dir, data_folder_dir_tmp)
    os.rename(data_folder_dir_tmp, data_folder_dir)
