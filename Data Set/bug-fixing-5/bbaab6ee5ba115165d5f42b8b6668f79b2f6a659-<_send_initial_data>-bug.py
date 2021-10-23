def _send_initial_data(self, fh, in_data):
    '\n        Writes initial data to the stdin filehandle of the subprocess and closes\n        it. (The handle must be closed; otherwise, for example, "sftp -b -" will\n        just hang forever waiting for more commands.)\n        '
    display.debug('Sending initial data')
    try:
        fh.write(to_bytes(in_data))
        fh.close()
    except (OSError, IOError):
        raise AnsibleConnectionFailure('SSH Error: data could not be sent to the remote host. Make sure this host can be reached over ssh')
    display.debug(('Sent initial data (%d bytes)' % len(in_data)))