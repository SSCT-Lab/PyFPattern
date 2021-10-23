

def createFontList(fontfiles, fontext='ttf'):
    '\n    A function to create a font lookup list.  The default is to create\n    a list of TrueType fonts.  An AFM font list can optionally be\n    created.\n    '
    fontlist = []
    seen = {
        
    }
    for fpath in fontfiles:
        verbose.report(('createFontDict: %s' % fpath), 'debug')
        fname = os.path.split(fpath)[1]
        if (fname in seen):
            continue
        else:
            seen[fname] = 1
        if (fontext == 'afm'):
            try:
                fh = open(fpath, 'rb')
            except:
                verbose.report(('Could not open font file %s' % fpath))
                continue
            try:
                try:
                    font = afm.AFM(fh)
                finally:
                    fh.close()
            except RuntimeError:
                verbose.report(('Could not parse font file %s' % fpath))
                continue
            try:
                prop = afmFontProperty(fpath, font)
            except KeyError:
                continue
        else:
            try:
                font = ft2font.FT2Font(fpath)
            except RuntimeError:
                verbose.report(('Could not open font file %s' % fpath))
                continue
            except UnicodeError:
                verbose.report('Cannot handle unicode filenames')
                continue
            try:
                prop = ttfFontProperty(font)
            except (KeyError, RuntimeError):
                continue
        fontlist.append(prop)
    return fontlist
