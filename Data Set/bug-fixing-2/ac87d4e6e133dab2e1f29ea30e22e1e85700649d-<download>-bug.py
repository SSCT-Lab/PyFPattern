

def download(self, hdfs_path, local_path, multi_processes=5, overwrite=False, retry_times=5):
    '\n        Download files from HDFS using multi process.\n\n        Args:\n            hdfs_path(str): path on hdfs\n            local_path(str): path on local\n            multi_processes(int|5): the download data process at the same time, default=5\n            overwrite(bool): is overwrite\n            retry_times(int): retry times\n\n        Returns:\n            List:\n            Download files in local folder.\n        '

    def __subprocess_download(local_path, datas):
        '\n            download file from HDFS\n\n            Args:\n                hdfs_path(str): the hdfs file path\n                local_path(str): the local file path\n                overwrite(bool|None): will overwrite the file on HDFS or not\n                retry_times(int|5): retry times\n\n            Returns:\n                True or False\n            '
        for data in datas:
            download_commands = ['-get', data, local_path]
            (returncode, output, errors) = self.__run_hdfs_cmd(download_commands, retry_times=retry_times)
            if returncode:
                _logger.error('Get local path: {} from HDFS path: {} failed'.format(local_path, hdfs_path))
                return False
        return True
    self.make_local_dirs(local_path)
    all_files = client.ls(hdfs_path)
    procs = []
    for i in range(multi_processes):
        process_datas = HDFSClient.split_files(all_files, i, multi_processes)
        p = multiprocessing.Process(target=__subprocess_download, args=(local_path, process_datas))
        procs.append(p)
        p.start()
    for proc in procs:
        proc.join()
    _logger.info('Finish {} multi process to download datas'.format(multi_processes))
    local_downloads = []
    for (dirname, folder, files) in os.walk(local_path):
        for i in files:
            t = os.path.join(dirname, i)
            local_downloads.append(t)
    return local_downloads
