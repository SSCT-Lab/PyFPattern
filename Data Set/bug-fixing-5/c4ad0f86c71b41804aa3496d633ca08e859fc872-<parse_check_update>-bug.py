def parse_check_update(check_update_output):
    updates = {
        
    }
    out = re.sub('\n[^\\w]\\W+(.*)', ' \x01', check_update_output)
    available_updates = out.split('\n')
    for line in available_updates:
        line = line.split()
        if (('*' in line) or (len(line) != 3) or ('.' not in line[0])):
            continue
        else:
            (pkg, version, repo) = line
            (name, dist) = pkg.rsplit('.', 1)
            updates.update({
                name: {
                    'version': version,
                    'dist': dist,
                    'repo': repo,
                },
            })
    return updates