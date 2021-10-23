@staticmethod
def guess_network_os(conn):
    (stdin, stdout, stderr) = conn.exec_command('cat /etc/issue')
    if ('VyOS' in stdout.read()):
        return 'vyos'