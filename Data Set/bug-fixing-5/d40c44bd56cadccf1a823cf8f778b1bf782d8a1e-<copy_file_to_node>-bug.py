def copy_file_to_node(module):
    " Copy config file to IOS-XR node. We use SFTP because older IOS-XR versions don't handle SCP very well.\n    "
    src = '/tmp/ansible_config.txt'
    file = open(src, 'wb')
    file.write(module.params['src'])
    file.close()
    dst = '/harddisk:/ansible_config.txt'
    copy_file(module, src, dst, 'sftp')
    return True