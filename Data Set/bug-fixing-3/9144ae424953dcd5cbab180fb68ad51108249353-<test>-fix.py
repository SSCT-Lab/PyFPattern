def test(file_list):
    process_result = True
    for file in file_list:
        with open(file, 'r') as src:
            if (not srccoms_extract(src, wlist)):
                process_result = False
    return process_result