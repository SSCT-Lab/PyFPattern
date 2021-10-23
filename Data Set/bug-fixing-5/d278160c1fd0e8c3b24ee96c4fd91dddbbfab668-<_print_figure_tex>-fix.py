def _print_figure_tex(self, outfile, format, dpi, facecolor, edgecolor, orientation, isLandscape, papertype, metadata=None, **kwargs):
    "\n        If text.usetex is True in rc, a temporary pair of tex/eps files\n        are created to allow tex to manage the text layout via the PSFrags\n        package. These files are processed to yield the final ps or eps file.\n\n        metadata must be a dictionary. Currently, only the value for\n        the key 'Creator' is used.\n        "
    isEPSF = (format == 'eps')
    if is_string_like(outfile):
        title = outfile
    elif is_writable_file_like(outfile):
        title = None
    else:
        raise ValueError('outfile must be a path or a file-like object')
    self.figure.dpi = 72
    (width, height) = self.figure.get_size_inches()
    xo = 0
    yo = 0
    (l, b, w, h) = self.figure.bbox.bounds
    llx = xo
    lly = yo
    urx = (llx + w)
    ury = (lly + h)
    bbox = (llx, lly, urx, ury)
    origfacecolor = self.figure.get_facecolor()
    origedgecolor = self.figure.get_edgecolor()
    self.figure.set_facecolor(facecolor)
    self.figure.set_edgecolor(edgecolor)
    dryrun = kwargs.get('dryrun', False)
    if dryrun:

        class NullWriter(object):

            def write(self, *kl, **kwargs):
                pass
        self._pswriter = NullWriter()
    else:
        self._pswriter = io.StringIO()
    _bbox_inches_restore = kwargs.pop('bbox_inches_restore', None)
    ps_renderer = self._renderer_class(width, height, self._pswriter, imagedpi=dpi)
    renderer = MixedModeRenderer(self.figure, width, height, dpi, ps_renderer, bbox_inches_restore=_bbox_inches_restore)
    self.figure.draw(renderer)
    if dryrun:
        return
    self.figure.set_facecolor(origfacecolor)
    self.figure.set_edgecolor(origedgecolor)
    if ((metadata is not None) and ('Creator' in metadata)):
        creator_str = metadata['Creator']
    else:
        creator_str = (('matplotlib version ' + __version__) + ', http://matplotlib.org/')
    (fd, tmpfile) = mkstemp()
    try:
        with io.open(fd, 'w', encoding='latin-1') as fh:
            print('%!PS-Adobe-3.0 EPSF-3.0', file=fh)
            if title:
                print(('%%Title: ' + title), file=fh)
            print(('%%Creator: ' + creator_str), file=fh)
            source_date_epoch = os.getenv('SOURCE_DATE_EPOCH')
            if source_date_epoch:
                source_date = datetime.datetime.utcfromtimestamp(int(source_date_epoch)).strftime('%a %b %d %H:%M:%S %Y')
            else:
                source_date = time.ctime()
            print(('%%CreationDate: ' + source_date), file=fh)
            print(('%%%%BoundingBox: %d %d %d %d' % bbox), file=fh)
            print('%%EndComments', file=fh)
            Ndict = len(psDefs)
            print('%%BeginProlog', file=fh)
            print(('/mpldict %d dict def' % Ndict), file=fh)
            print('mpldict begin', file=fh)
            for d in psDefs:
                d = d.strip()
                for l in d.split('\n'):
                    print(l.strip(), file=fh)
            print('end', file=fh)
            print('%%EndProlog', file=fh)
            print('mpldict begin', file=fh)
            print(('%s translate' % _nums_to_str(xo, yo)), file=fh)
            print(('%s clipbox' % _nums_to_str((width * 72), (height * 72), 0, 0)), file=fh)
            print(self._pswriter.getvalue(), file=fh)
            print('end', file=fh)
            print('showpage', file=fh)
            fh.flush()
        if isLandscape:
            isLandscape = True
            (width, height) = (height, width)
            bbox = (lly, llx, ury, urx)
        if isEPSF:
            (paperWidth, paperHeight) = self.figure.get_size_inches()
            if isLandscape:
                (paperWidth, paperHeight) = (paperHeight, paperWidth)
        else:
            temp_papertype = _get_papertype(width, height)
            if (papertype == 'auto'):
                papertype = temp_papertype
                (paperWidth, paperHeight) = papersize[temp_papertype]
            else:
                (paperWidth, paperHeight) = papersize[papertype]
                if (((width > paperWidth) or (height > paperHeight)) and isEPSF):
                    (paperWidth, paperHeight) = papersize[temp_papertype]
                    verbose.report(('Your figure is too big to fit on %s paper. %s paper will be used to prevent clipping.' % (papertype, temp_papertype)), 'helpful')
        texmanager = ps_renderer.get_texmanager()
        font_preamble = texmanager.get_font_preamble()
        custom_preamble = texmanager.get_custom_preamble()
        psfrag_rotated = convert_psfrags(tmpfile, ps_renderer.psfrag, font_preamble, custom_preamble, paperWidth, paperHeight, orientation)
        if (rcParams['ps.usedistiller'] == 'ghostscript'):
            gs_distill(tmpfile, isEPSF, ptype=papertype, bbox=bbox, rotated=psfrag_rotated)
        elif (rcParams['ps.usedistiller'] == 'xpdf'):
            xpdf_distill(tmpfile, isEPSF, ptype=papertype, bbox=bbox, rotated=psfrag_rotated)
        elif rcParams['text.usetex']:
            if False:
                pass
            else:
                gs_distill(tmpfile, isEPSF, ptype=papertype, bbox=bbox, rotated=psfrag_rotated)
        if is_writable_file_like(outfile):
            if file_requires_unicode(outfile):
                with io.open(tmpfile, 'rb') as fh:
                    outfile.write(fh.read().decode('latin-1'))
            else:
                with io.open(tmpfile, 'rb') as fh:
                    outfile.write(fh.read())
        else:
            with io.open(outfile, 'wb') as fh:
                pass
            mode = os.stat(outfile).st_mode
            shutil.move(tmpfile, outfile)
            os.chmod(outfile, mode)
    finally:
        if os.path.isfile(tmpfile):
            os.unlink(tmpfile)