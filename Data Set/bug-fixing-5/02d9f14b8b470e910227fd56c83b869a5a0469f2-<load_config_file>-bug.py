def load_config_file():
    ' Load Config File order(first found is used): ENV, CWD, HOME, /etc/ansible '
    p = configparser.ConfigParser()
    path0 = os.getenv('ANSIBLE_CONFIG', None)
    if (path0 is not None):
        path0 = os.path.expanduser(path0)
        if os.path.isdir(path0):
            path0 += '/ansible.cfg'
    path1 = (os.getcwd() + '/ansible.cfg')
    path2 = os.path.expanduser('~/.ansible.cfg')
    path3 = '/etc/ansible/ansible.cfg'
    for path in [path0, path1, path2, path3]:
        if ((path is not None) and os.path.exists(path)):
            try:
                p.read(path)
            except configparser.Error as e:
                raise AnsibleOptionsError('Error reading config file: \n{0}'.format(e))
            return (p, path)
    return (None, '')