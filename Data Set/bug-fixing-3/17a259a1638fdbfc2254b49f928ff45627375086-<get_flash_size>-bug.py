def get_flash_size(module):
    command = 'dir {}'.format(module.params['file_system'])
    body = run_commands(module, [command])[0]
    match = re.search('(\\d+) bytes free', body)
    bytes_free = match.group(1)
    return int(bytes_free)