def vlan_vid_to_bitmap(vid):
    'convert VLAN list to VLAN bitmap'
    vlan_bit = (['0'] * 1024)
    int_vid = int(vid)
    j = (int_vid // 4)
    bit_int = (8 >> (int_vid % 4))
    vlan_bit[j] = str(hex(bit_int))[2]
    return ''.join(vlan_bit)