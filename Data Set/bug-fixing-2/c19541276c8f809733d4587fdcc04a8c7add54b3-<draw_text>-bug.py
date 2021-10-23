

def draw_text(self, gc, x, y, s, prop, angle, ismath=False, mtext=None):
    s = common_texification(s)
    prop_cmds = _font_properties_str(prop)
    s = ('%s %s' % (prop_cmds, s))
    writeln(self.fh, '\\begin{pgfscope}')
    alpha = gc.get_alpha()
    if (alpha != 1.0):
        writeln(self.fh, ('\\pgfsetfillopacity{%f}' % alpha))
        writeln(self.fh, ('\\pgfsetstrokeopacity{%f}' % alpha))
    rgb = tuple(gc.get_rgb())[:3]
    if (rgb != (0, 0, 0)):
        writeln(self.fh, ('\\definecolor{textcolor}{rgb}{%f,%f,%f}' % rgb))
        writeln(self.fh, '\\pgfsetstrokecolor{textcolor}')
        writeln(self.fh, '\\pgfsetfillcolor{textcolor}')
        s = ('\\color{textcolor}' + s)
    f = (1.0 / self.figure.dpi)
    text_args = []
    if (mtext and (((angle == 0) or (mtext.get_rotation_mode() == 'anchor')) and (mtext.get_va() != 'center_baseline'))):
        (x, y) = mtext.get_transform().transform_point(mtext.get_position())
        text_args.append(('x=%fin' % (x * f)))
        text_args.append(('y=%fin' % (y * f)))
        halign = {
            'left': 'left',
            'right': 'right',
            'center': '',
        }
        valign = {
            'top': 'top',
            'bottom': 'bottom',
            'baseline': 'base',
            'center': '',
        }
        text_args.append(halign[mtext.get_ha()])
        text_args.append(valign[mtext.get_va()])
    else:
        text_args.append(('x=%fin' % (x * f)))
        text_args.append(('y=%fin' % (y * f)))
        text_args.append('left')
        text_args.append('base')
    if (angle != 0):
        text_args.append(('rotate=%f' % angle))
    writeln(self.fh, ('\\pgftext[%s]{%s}' % (','.join(text_args), s)))
    writeln(self.fh, '\\end{pgfscope}')
