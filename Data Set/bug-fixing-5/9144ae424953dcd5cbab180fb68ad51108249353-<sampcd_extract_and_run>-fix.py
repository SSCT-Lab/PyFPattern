def sampcd_extract_and_run(srccom, name, htype='def', hname=''):
    '\n    Extract and run sample codes from source comment and\n    the result will be returned.\n\n    Args:\n        srccom(str): the source comment of some API whose\n                     example codes will be extracted and run.\n        name(str): the name of the API.\n        htype(str): the type of hint banners, def/class/method.\n        hname(str): the name of the hint  banners , e.t. def hname.\n\n    Returns:\n        result: True or False\n    '
    result = True

    def sampcd_header_print(name, sampcd, htype, hname):
        '\n        print hint banner headers.\n\n        Args:\n            name(str): the name of the API.\n            sampcd(str): sample code string\n            htype(str): the type of hint banners, def/class/method.\n            hname(str): the name of the hint  banners , e.t. def hname.\n            flushed.\n        '
        print_header(htype, hname)
        print('Sample code ', str(y), ' extracted for ', name, '   :')
        print(sampcd)
        print('----example code check----\n')
        print('executing sample code .....')
        print('execution result:')
    sampcd_begins = find_all(srccom, ' code-block:: python')
    if (len(sampcd_begins) == 0):
        print_header(htype, hname)
        '\n        detect sample codes using >>> to format\n        and consider this situation as wrong\n        '
        if (srccom.find('Examples:') != (- 1)):
            print('----example code check----\n')
            if (srccom.find('>>>') != (- 1)):
                print('Deprecated sample code style:\n\n    Examples:\n\n        >>>codeline\n        >>>codeline\n\n\n ', "Please use '.. code-block:: python' to ", 'format sample code.\n')
                result = False
        else:
            print('Error: No sample code!\n')
            result = False
    for y in range(1, (len(sampcd_begins) + 1)):
        sampcd_begin = sampcd_begins[(y - 1)]
        sampcd = srccom[((sampcd_begin + len(' code-block:: python')) + 1):]
        sampcd = sampcd.split('\n')
        while (sampcd[0].replace(' ', '').replace('\t', '') == ''):
            sampcd.pop(0)
        min_indent = check_indent(sampcd[0])
        sampcd_to_write = []
        for i in range(0, len(sampcd)):
            cdline = sampcd[i]
            if (cdline.strip() == ''):
                continue
            this_indent = check_indent(cdline)
            if (this_indent < min_indent):
                break
            else:
                cdline = cdline.replace('\t', '    ')
                sampcd_to_write.append(cdline[min_indent:])
        sampcd = '\n'.join(sampcd_to_write)
        if (sys.argv[1] == 'cpu'):
            sampcd = (('\nimport os\n' + 'os.environ["CUDA_VISIBLE_DEVICES"] = ""\n') + sampcd)
        if (sys.argv[1] == 'gpu'):
            sampcd = (('\nimport os\n' + 'os.environ["CUDA_VISIBLE_DEVICES"] = "0"\n') + sampcd)
        sampcd += ((('\nprint(' + '"') + name) + ' sample code is executed successfully!")')
        if (len(sampcd_begins) > 1):
            tfname = (((name + '_example_') + str(y)) + '.py')
        else:
            tfname = ((name + '_example') + '.py')
        tempf = open(('samplecode_temp/' + tfname), 'w')
        tempf.write(sampcd)
        tempf.close()
        if (platform.python_version()[0] == '2'):
            cmd = ['python', ('samplecode_temp/' + tfname)]
        elif (platform.python_version()[0] == '3'):
            cmd = ['python3', ('samplecode_temp/' + tfname)]
        else:
            print('Error: fail to parse python version!')
            result = False
            exit(1)
        subprc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        (output, error) = subprc.communicate()
        msg = ''.join(output.decode(encoding='utf-8'))
        err = ''.join(error.decode(encoding='utf-8'))
        if (subprc.returncode != 0):
            print('\nSample code error found in ', name, ':\n')
            sampcd_header_print(name, sampcd, htype, hname)
            print('subprocess return code: ', str(subprc.returncode))
            print('Error Raised from Sample Code ', name, ' :\n')
            print(err)
            print(msg)
            result = False
        os.remove(('samplecode_temp/' + tfname))
    return result