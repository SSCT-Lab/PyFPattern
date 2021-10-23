def icmp_present(entry):
    if (((len(entry) == 6) and (entry[1] == 'icmp')) or (entry[1] == 1)):
        return True