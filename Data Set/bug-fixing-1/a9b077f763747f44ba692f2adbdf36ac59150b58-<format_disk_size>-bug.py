

def format_disk_size(size_bytes, unit):
    "\n    Formats a size in bytes into a different unit, like parted does. It doesn't\n    manage CYL and CHS formats, though.\n    This function has been adapted from https://github.com/Distrotech/parted/blo\n    b/279d9d869ff472c52b9ec2e180d568f0c99e30b0/libparted/unit.c\n    "
    global units_si, units_iec
    unit = unit.lower()
    if (size_bytes == 0):
        return 0.0
    if (unit in ['', 'compact', 'cyl', 'chs']):
        index = max(0, int(((math.log10(size_bytes) - 1.0) / 3.0)))
        unit = 'b'
        if (index < len(units_si)):
            unit = units_si[index]
    multiplier = 1.0
    if (unit in units_si):
        multiplier = (1000.0 ** units_si.index(unit))
    elif (unit in units_iec):
        multiplier = (1024.0 ** units_iec.index(unit))
    output = ((size_bytes // multiplier) * (1 + 1e-16))
    if (output < 10):
        w = (output + 0.005)
    elif (output < 100):
        w = (output + 0.05)
    else:
        w = (output + 0.5)
    if (w < 10):
        precision = 2
    elif (w < 100):
        precision = 1
    else:
        precision = 0
    return (round(output, precision), unit)
