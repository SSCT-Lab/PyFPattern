

def get_redirected_output(path_name):
    output = []
    with open(path_name, 'r') as fd:
        for line in fd:
            new_line = re.sub('\\x1b\\[.+m', '', line)
            output.append(new_line)
    fd.close()
    os.remove(path_name)
    return output
