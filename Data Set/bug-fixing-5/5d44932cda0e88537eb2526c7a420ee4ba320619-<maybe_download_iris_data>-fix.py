def maybe_download_iris_data(file_name, download_url):
    'Downloads the file and returns the number of data.'
    if (not os.path.exists(file_name)):
        urlretrieve(download_url, file_name)
    with open(file_name, 'r') as f:
        first_line = f.readline()
    num_elements = first_line.split(',')[0]
    return int(num_elements)