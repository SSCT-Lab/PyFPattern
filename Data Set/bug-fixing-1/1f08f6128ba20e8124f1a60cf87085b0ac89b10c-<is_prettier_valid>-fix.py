

def is_prettier_valid(project_root, prettier_path):
    if (not os.path.exists(prettier_path)):
        echo('[sentry.lint] Skipping JavaScript formatting because prettier is not installed.', err=True)
        return False
    package_version = None
    package_json_path = os.path.join(project_root, 'package.json')
    with open(package_json_path) as package_json:
        try:
            package_version = json.load(package_json)['devDependencies']['prettier']
        except KeyError:
            echo('!! Prettier missing from package.json', err=True)
            return False
    prettier_version = subprocess.check_output([prettier_path, '--version']).rstrip()
    if (prettier_version != package_version):
        echo('[sentry.lint] Prettier is out of date: {} (expected {}). Please run `yarn install`.'.format(prettier_version, package_version), err=True)
        return False
    return True
