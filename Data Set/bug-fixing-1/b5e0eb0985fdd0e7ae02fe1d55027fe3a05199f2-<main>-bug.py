

def main():
    targets_dir = 'test/integration/targets'
    with open('test/integration/target-prefixes.network', 'r') as prefixes_fd:
        network_prefixes = prefixes_fd.read().splitlines()
    missing_aliases = []
    for target in sorted(os.listdir(targets_dir)):
        target_dir = os.path.join(targets_dir, target)
        aliases_path = os.path.join(target_dir, 'aliases')
        files = sorted(os.listdir(target_dir))
        if os.path.exists(aliases_path):
            continue
        if any(((os.path.splitext(f)[0] == 'test') for f in files)):
            continue
        if target.startswith('setup_'):
            continue
        if target.startswith('prepare_'):
            continue
        if any((target.startswith(('%s_' % prefix)) for prefix in network_prefixes)):
            continue
        missing_aliases.append(target_dir)
    if missing_aliases:
        message = ("\n        The following integration target directories are missing `aliases` files:\n\n        %s\n\n        Unless a test cannot run as part of CI, you'll want to add an appropriate CI alias, such as:\n\n        posix/ci/group1\n        windows/ci/group2\n\n        The CI groups are used to balance tests across multiple jobs to minimize test run time.\n\n        Aliases can also be used to express test requirements:\n\n        needs/privileged\n        needs/root\n        needs/ssh\n\n        Other aliases are used to skip tests under certain conditions:\n\n        skip/freebsd\n        skip/osx\n        skip/python3\n\n        Take a look at existing `aliases` files to see what aliases are available and how they're used.\n        " % '\n'.join(missing_aliases))
        print(textwrap.dedent(message).strip())
        exit(1)
