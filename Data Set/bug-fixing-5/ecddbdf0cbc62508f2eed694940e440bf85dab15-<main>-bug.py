def main():
    'Main program function.'
    base_dir = os.getcwd()
    messages = set()
    if AnsibleCollectionLoader:
        sys.meta_path.insert(0, AnsibleCollectionLoader())
    for path in (sys.argv[1:] or sys.stdin.read().splitlines()):
        test_python_module(path, base_dir, messages, False)
        test_python_module(path, base_dir, messages, True)
    if messages:
        exit(10)