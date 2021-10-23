def extract_contents(args, path, output_dir):
    if (not args.test):
        with open(path, 'r') as json_fd:
            items = json.load(json_fd)
            for item in items:
                contents = item['contents']
                path = ((output_dir + '/') + re.sub('^/*', '', item['path']))
                directory = os.path.dirname(path)
                if (not os.path.exists(directory)):
                    os.makedirs(directory)
                if args.verbose:
                    print(path)
                if (not os.path.exists(path)):
                    with open(path, 'w') as output_fd:
                        output_fd.write(contents)