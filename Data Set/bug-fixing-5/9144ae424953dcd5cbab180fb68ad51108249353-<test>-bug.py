def test(file_list):
    for file in file_list:
        src = open(file, 'r')
        counts = srccoms_extract(src, status_all, wlist)
        src.close()