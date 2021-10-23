

def get_self_heal_status(name):
    out = run_gluster(['volume', 'heal', name, 'info'], environ_update=dict(LANG='C', LC_ALL='C', LC_MESSAGES='C'))
    raw_out = out.split('\n')
    heal_info = []
    for line in raw_out:
        if ('Brick' in line):
            br_dict = {
                
            }
            br_dict['brick'] = line.strip().strip('Brick')
        elif ('Status' in line):
            br_dict['status'] = line.split(':')[1].strip()
        elif ('Number' in line):
            br_dict['no_of_entries'] = line.split(':')[1].strip()
        elif (line.startswith('/') or line.startswith('<') or ('\n' in line)):
            continue
        else:
            (br_dict and heal_info.append(br_dict))
            br_dict = {
                
            }
    return heal_info
