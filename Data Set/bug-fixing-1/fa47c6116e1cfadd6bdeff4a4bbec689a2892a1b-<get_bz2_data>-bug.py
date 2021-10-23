

def get_bz2_data(data_dir, data_name, url, data_origin_name):
    'Download and extract bz2 data.'
    download(url, dirname=data_dir, overwrite=False)
    os.chdir(data_dir)
    if (not os.path.exists(data_name)):
        bz_file = bz2.BZ2File(data_origin_name, 'rb')
        with open(data_name, 'wb') as fout:
            try:
                content = bz_file.read()
                fout.write(content)
            finally:
                bz_file.close()
        os.remove(data_origin_name)
    os.chdir('..')
