def get_state(b_path):
    ' Find out current state '
    if os.path.lexists(b_path):
        if os.path.islink(b_path):
            return 'link'
        elif os.path.isdir(b_path):
            return 'directory'
        elif (os.stat(b_path).st_nlink > 1):
            return 'hard'
        else:
            return 'file'
    return 'absent'