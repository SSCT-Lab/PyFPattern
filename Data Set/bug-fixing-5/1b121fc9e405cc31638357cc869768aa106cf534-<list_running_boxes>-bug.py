def list_running_boxes():
    output = subprocess.check_output(['vagrant', 'status']).split('\n')
    boxes = []
    for line in output:
        matcher = re.search('([^\\s]+)[\\s]+running \\(.+', line)
        if matcher:
            boxes.append(matcher.group(1))
    return boxes