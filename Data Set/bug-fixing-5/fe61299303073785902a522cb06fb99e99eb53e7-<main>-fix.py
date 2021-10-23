def main():
    cmds = [method for method in dir(DocBuilder) if (not method.startswith('_'))]
    argparser = argparse.ArgumentParser(description='pandas documentation builder', epilog='Commands: {}'.format(','.join(cmds)))
    argparser.add_argument('command', nargs='?', default='html', help='command to run: {}'.format(', '.join(cmds)))
    argparser.add_argument('--num-jobs', type=int, default=1, help='number of jobs used by sphinx-build')
    argparser.add_argument('--no-api', default=False, help='ommit api and autosummary', action='store_true')
    argparser.add_argument('--single', metavar='FILENAME', type=str, default=None, help='filename of section or method name to compile, e.g. "indexing", "DataFrame.join"')
    argparser.add_argument('--python-path', type=str, default=os.path.dirname(DOC_PATH), help='path')
    argparser.add_argument('-v', action='count', dest='verbosity', default=0, help='increase verbosity (can be repeated), passed to the sphinx build command')
    args = argparser.parse_args()
    if (args.command not in cmds):
        raise ValueError('Unknown command {}. Available options: {}'.format(args.command, ', '.join(cmds)))
    os.environ['PYTHONPATH'] = args.python_path
    sys.path.append(args.python_path)
    globals()['pandas'] = importlib.import_module('pandas')
    builder = DocBuilder(args.num_jobs, (not args.no_api), args.single, args.verbosity)
    getattr(builder, args.command)()