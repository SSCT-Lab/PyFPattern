def main():
    errors = []
    pattern = re.compile('^./test/integration/targets/.*/backup')
    for (root, dirs, files) in os.walk('.'):
        if pattern.match(root):
            continue
        for dir_name in dirs:
            errors += check_path(os.path.abspath(os.path.join(root, dir_name)), dir=True)
        for file_name in files:
            errors += check_path(os.path.abspath(os.path.join(root, file_name)), dir=False)
    if (len(errors) > 0):
        print('Ansible git repo should not contain any illegal filenames')
        for error in errors:
            print(error)
        exit(1)