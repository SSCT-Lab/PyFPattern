def list_running_boxes():
    output = to_text(subprocess.check_output(['vagrant', 'status']), errors='surrogate_or_strict').split('\n')
    boxes = []
    for line in output:
        matcher = re.search('([^\\s]+)[\\s]+running \\(.+', line)
        if matcher:
            boxes.append(matcher.group(1))
    return boxes