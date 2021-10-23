

def vlan_range_to_list(vlans):
    result = []
    if vlans:
        for part in vlans.split(','):
            if (part.lower() == 'none'):
                break
            if part:
                if ('-' in part):
                    (start, stop) = (int(i) for i in part.split('-'))
                    result.extend(range(start, (stop + 1)))
                else:
                    result.append(int(part))
    return sorted(result)
