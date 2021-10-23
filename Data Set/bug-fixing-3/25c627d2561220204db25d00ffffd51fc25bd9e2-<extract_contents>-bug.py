def extract_contents(args, path, output_dir):
    '\n    :type args: any\n    :type path: str\n    :type output_dir: str\n    '
    if (not args.test):
        if (not os.path.exists(path)):
            return
        with open(path, 'r') as json_fd:
            items = json.load(json_fd)
            for item in items:
                contents = item['contents'].encode('utf-8')
                path = ((output_dir + '/') + re.sub('^/*', '', item['path']))
                directory = os.path.dirname(path)
                if (not os.path.exists(directory)):
                    os.makedirs(directory)
                if args.verbose:
                    print(path)
                if path.endswith('.json'):
                    contents = json.dumps(json.loads(contents), sort_keys=True, indent=4)
                if (not os.path.exists(path)):
                    with open(path, 'w') as output_fd:
                        output_fd.write(contents)