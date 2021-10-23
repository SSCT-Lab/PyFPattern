@staticmethod
def guess_network_os(conn):
    (stdin, stdout, stderr) = conn.exec_command('cat /proc/version')
    if ('vyos' in stdout.read()):
        return 'vyos'