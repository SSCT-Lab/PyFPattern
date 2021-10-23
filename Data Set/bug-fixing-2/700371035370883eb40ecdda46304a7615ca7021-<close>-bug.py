

def close(self):
    '\n        Close and upload local log file to remote storage S3.\n        '
    if self.closed:
        return
    super().close()
    if (not self.upload_on_close):
        return
    local_loc = os.path.join(self.local_base, self.log_relative_path)
    remote_loc = os.path.join(self.remote_base, self.log_relative_path)
    if os.path.exists(local_loc):
        with open(local_loc, 'r') as logfile:
            log = logfile.read()
        self.gcs_write(log, remote_loc)
    self.closed = True
