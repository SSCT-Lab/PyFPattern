def get_version(pacman_output):
    'Take pacman -Qi or pacman -Si output and get the Version'
    lines = pacman_output.split('\n')
    for line in lines:
        if line.startswith('Version '):
            return line.split(':')[1].strip()
    return None