def parse_partition_info(parted_output, unit):
    '\n    Parses the output of parted and transforms the data into\n    a dictionary.\n\n    Parted Machine Parseable Output:\n    See: https://lists.alioth.debian.org/pipermail/parted-devel/2006-December/00\n    0573.html\n     - All lines end with a semicolon (;)\n     - The first line indicates the units in which the output is expressed.\n       CHS, CYL and BYT stands for CHS, Cylinder and Bytes respectively.\n     - The second line is made of disk information in the following format:\n       "path":"size":"transport-type":"logical-sector-size":"physical-sector-siz\n       e":"partition-table-type":"model-name";\n     - If the first line was either CYL or CHS, the next line will contain\n       information on no. of cylinders, heads, sectors and cylinder size.\n     - Partition information begins from the next line. This is of the format:\n       (for BYT)\n       "number":"begin":"end":"size":"filesystem-type":"partition-name":"flags-s\n       et";\n       (for CHS/CYL)\n       "number":"begin":"end":"filesystem-type":"partition-name":"flags-set";\n    '
    lines = [x for x in parted_output.split('\n') if (x.strip() != '')]
    generic_params = lines[1].rstrip(';').split(':')
    (size, unit) = parse_unit(generic_params[1], unit)
    generic = {
        'dev': generic_params[0],
        'size': size,
        'unit': unit.lower(),
        'table': generic_params[5],
        'model': generic_params[6],
        'logical_block': int(generic_params[3]),
        'physical_block': int(generic_params[4]),
    }
    if (unit in ['cyl', 'chs']):
        chs_info = lines[2].rstrip(';').split(':')
        (cyl_size, cyl_unit) = parse_unit(chs_info[3])
        generic['chs_info'] = {
            'cylinders': int(chs_info[0]),
            'heads': int(chs_info[1]),
            'sectors': int(chs_info[2]),
            'cyl_size': cyl_size,
            'cyl_size_unit': cyl_unit.lower(),
        }
        lines = lines[1:]
    parts = []
    for line in lines[2:]:
        part_params = line.rstrip(';').split(':')
        if (unit != 'chs'):
            size = parse_unit(part_params[3])[0]
            fstype = part_params[4]
            name = part_params[5]
            flags = part_params[6]
        else:
            size = ''
            fstype = part_params[3]
            name = part_params[4]
            flags = part_params[5]
        parts.append({
            'num': int(part_params[0]),
            'begin': parse_unit(part_params[1])[0],
            'end': parse_unit(part_params[2])[0],
            'size': size,
            'fstype': fstype,
            'name': name,
            'flags': [f.strip() for f in flags.split(', ') if (f != '')],
            'unit': unit.lower(),
        })
    return {
        'generic': generic,
        'partitions': parts,
    }