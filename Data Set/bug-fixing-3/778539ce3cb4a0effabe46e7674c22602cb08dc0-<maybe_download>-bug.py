def maybe_download(filename, work_directory, source_url):
    "Download the data from source url, unless it's already here.\n\n  Args:\n      filename: string, name of the file in the directory.\n      work_directory: string, path to working directory.\n      source_url: url to download from if file doesn't exist.\n\n  Returns:\n      Path to resulting file.\n  "
    if (not gfile.Exists(work_directory)):
        gfile.MakeDirs(work_directory)
    filepath = os.path.join(work_directory, filename)
    if (not gfile.Exists(filepath)):
        with tempfile.NamedTemporaryFile() as tmpfile:
            temp_file_name = tmpfile.name
            urlretrieve_with_retry(source_url, temp_file_name)
            gfile.Copy(temp_file_name, filepath)
            with gfile.GFile(filepath) as f:
                size = f.size()
            print('Successfully downloaded', filename, size, 'bytes.')
    return filepath