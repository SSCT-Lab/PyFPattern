def check_command(module, commandline):
    arguments = {
        'chown': 'owner',
        'chmod': 'mode',
        'chgrp': 'group',
        'ln': 'state=link',
        'mkdir': 'state=directory',
        'rmdir': 'state=absent',
        'rm': 'state=absent',
        'touch': 'state=touch',
    }
    commands = {
        'hg': 'hg',
        'curl': 'get_url or uri',
        'wget': 'get_url or uri',
        'svn': 'subversion',
        'service': 'service',
        'mount': 'mount',
        'rpm': 'yum, dnf or zypper',
        'yum': 'yum',
        'apt-get': 'apt',
        'tar': 'unarchive',
        'unzip': 'unarchive',
        'sed': 'template or lineinfile',
        'dnf': 'dnf',
        'zypper': 'zypper',
    }
    become = ['sudo', 'su', 'pbrun', 'pfexec', 'runas', 'pmrun']
    command = os.path.basename(commandline.split()[0])
    if (command in arguments):
        module.warn(('Consider using file module with %s rather than running %s' % (arguments[command], command)))
    if (command in commands):
        module.warn(('Consider using %s module rather than running %s' % (commands[command], command)))
    if (command in become):
        module.warn(("Consider using 'become', 'become_method', and 'become_user' rather than running %s" % (command,)))