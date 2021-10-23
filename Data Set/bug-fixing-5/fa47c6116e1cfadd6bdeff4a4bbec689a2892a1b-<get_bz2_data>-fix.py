def get_bz2_data(data_dir, data_name, url, data_origin_name):
    'Download and extract bz2 data.\n\n    Parameters\n    ----------\n\n    data_dir : str\n        Absolute or relative path of the directory name to store bz2 files\n    data_name : str\n        Name of the output file in which bz2 contents will be extracted\n    url : str\n        URL to download data from\n    data_origin_name : str\n        Name of the downloaded b2 file\n\n    Examples\n    --------\n    >>> get_bz2_data("data_dir", "kdda.t",\n                     "https://www.csie.ntu.edu.tw/~cjlin/libsvmtools/datasets/binary/kdda.t.bz2",\n                     "kdda.t.bz2")\n    '
    data_name = os.path.join(data_dir, data_name)
    data_origin_name = os.path.join(data_dir, data_origin_name)
    if (not os.path.exists(data_name)):
        download(url, dirname=data_dir, overwrite=False)
        bz_file = bz2.BZ2File(data_origin_name, 'rb')
        with open(data_name, 'wb') as fout:
            try:
                content = bz_file.read()
                fout.write(content)
            finally:
                bz_file.close()
        os.remove(data_origin_name)