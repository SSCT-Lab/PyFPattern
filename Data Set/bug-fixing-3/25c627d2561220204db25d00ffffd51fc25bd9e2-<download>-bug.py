def download(args, headers, path, url, is_json=True):
    '\n    :type args: any\n    :type headers: dict[str, str]\n    :type path: str\n    :type url: str\n    :type is_json: bool\n    '
    if (args.verbose or args.test):
        print(path)
    if os.path.exists(path):
        return
    if (not args.test):
        response = requests.get(url, headers=headers)
        if (response.status_code != 200):
            path += '.error'
        if is_json:
            content = json.dumps(response.json(), sort_keys=True, indent=4)
        else:
            content = response.content
        directory = os.path.dirname(path)
        if (not os.path.exists(directory)):
            os.makedirs(directory)
        with open(path, 'w') as content_fd:
            content_fd.write(content)