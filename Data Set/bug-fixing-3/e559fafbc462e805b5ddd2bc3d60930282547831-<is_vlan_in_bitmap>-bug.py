def is_vlan_in_bitmap(vid, bitmap):
    'check is VLAN id in bitmap'
    if is_vlan_bitmap_empty(bitmap):
        return False
    i = (int(vid) / 4)
    if (i > len(bitmap)):
        return False
    if (int(bitmap[i]) & (8 >> (int(vid) % 4))):
        return True
    return False