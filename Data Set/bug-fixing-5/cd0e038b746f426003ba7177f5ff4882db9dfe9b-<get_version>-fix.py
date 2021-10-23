def get_version(pacman_output, from_sync=False):
    'Take pacman -Qi or pacman -Si output and get the Version'
    lines = pacman_output.split('\n')
    index = 1
    if from_sync:
        index = 2
    try:
        version = lines[index].split(':')[1].strip()
    except IndexError:
        version = None
    return version