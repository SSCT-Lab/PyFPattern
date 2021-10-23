def write_all_rst_pages():
    ' Do the main task of writing the gallery, detail, and index rst pages '
    infos = get_infos(screenshots_dir)
    s = make_gallery_page(infos)
    write_file(gallery_filename, s)
    for info in infos:
        s = make_detail_page(info)
        detail_name = slash(generation_dir, 'gen__{}.rst'.format(info['dunder']))
        write_file(detail_name, s)
    s = make_index(infos)
    index_name = slash(generation_dir, 'index.rst')
    write_file(index_name, s)
    Logger.info('gallery.py: Created gallery rst documentation pages.')