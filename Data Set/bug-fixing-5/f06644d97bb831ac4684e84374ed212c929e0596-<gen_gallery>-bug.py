def gen_gallery(app, doctree):
    if (app.builder.name not in ('html', 'htmlhelp')):
        return
    outdir = app.builder.outdir
    rootdir = 'plot_directive/mpl_examples'
    example_sections = list(app.builder.config.mpl_example_sections)
    for (i, (subdir, title)) in enumerate(example_sections):
        if (subdir in exclude_example_sections):
            example_sections.pop(i)
    skips = set(['mathtext_examples', 'matshow_02', 'matshow_03', 'matplotlib_icon'])
    thumbnails = {
        
    }
    rows = []
    toc_rows = []
    for (subdir, title) in example_sections:
        rows.append(header_template.format(title=title, section=subdir))
        toc_rows.append(toc_template.format(title=title, section=subdir))
        origdir = os.path.join('build', rootdir, subdir)
        thumbdir = os.path.join(outdir, rootdir, subdir, 'thumbnails')
        if (not os.path.exists(thumbdir)):
            os.makedirs(thumbdir)
        data = []
        for filename in sorted(glob.glob(os.path.join(origdir, '*.png'))):
            if filename.endswith('hires.png'):
                continue
            (path, filename) = os.path.split(filename)
            (basename, ext) = os.path.splitext(filename)
            if (basename in skips):
                continue
            orig_path = str(os.path.join(origdir, filename))
            thumb_path = str(os.path.join(thumbdir, filename))
            if (out_of_date(orig_path, thumb_path) or True):
                thumbnails[orig_path] = thumb_path
            m = multiimage.match(basename)
            if (m is not None):
                basename = m.group(1)
            data.append((subdir, basename, os.path.join(rootdir, subdir, 'thumbnails', filename)))
        for (subdir, basename, thumbfile) in data:
            if (thumbfile is not None):
                link = ('examples/%s/%s.html' % (subdir, basename))
                rows.append(link_template.format(link=link, thumb=thumbfile, basename=basename, title=basename))
        if (len(data) == 0):
            warnings.warn(('No thumbnails were found in %s' % subdir))
        rows.append('</div>')
    content = gallery_template.format(toc='\n'.join(toc_rows), gallery='\n'.join(rows))
    gallery_path = os.path.join(app.builder.srcdir, '_templates', 'gallery.html')
    if os.path.exists(gallery_path):
        fh = open(gallery_path, 'r')
        regenerate = (fh.read() != content)
        fh.close()
    else:
        regenerate = True
    if regenerate:
        fh = open(gallery_path, 'w')
        fh.write(content)
        fh.close()
    for key in app.builder.status_iterator(iter(thumbnails.keys()), 'generating thumbnails... ', length=len(thumbnails)):
        if out_of_date(key, thumbnails[key]):
            image.thumbnail(key, thumbnails[key], 0.3)