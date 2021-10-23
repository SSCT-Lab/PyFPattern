def draw_markers(self, gc, marker_path, marker_trans, path, trans, rgbFace=None):
    '\n        Draw the markers defined by path at each of the positions in x\n        and y.  path coordinates are points, x and y coords will be\n        transformed by the transform\n        '
    if debugPS:
        self._pswriter.write('% draw_markers \n')
    if rgbFace:
        if ((len(rgbFace) == 4) and (rgbFace[3] == 0)):
            ps_color = None
        elif (rgbFace[0] == rgbFace[1] == rgbFace[2]):
            ps_color = ('%1.3f setgray' % rgbFace[0])
        else:
            ps_color = ('%1.3f %1.3f %1.3f setrgbcolor' % rgbFace[:3])
    ps_cmd = ['/o {', 'gsave', 'newpath', 'translate']
    lw = gc.get_linewidth()
    stroke = (lw != 0.0)
    if stroke:
        ps_cmd.append(('%.1f setlinewidth' % lw))
        jint = gc.get_joinstyle()
        ps_cmd.append(('%d setlinejoin' % jint))
        cint = gc.get_capstyle()
        ps_cmd.append(('%d setlinecap' % cint))
    ps_cmd.append(self._convert_path(marker_path, marker_trans, simplify=False))
    if rgbFace:
        if stroke:
            ps_cmd.append('gsave')
        if ps_color:
            ps_cmd.extend([ps_color, 'fill'])
        if stroke:
            ps_cmd.append('grestore')
    if stroke:
        ps_cmd.append('stroke')
    ps_cmd.extend(['grestore', '} bind def'])
    for (vertices, code) in path.iter_segments(trans, clip=(0, 0, (self.width * 72), (self.height * 72)), simplify=False):
        if len(vertices):
            (x, y) = vertices[(- 2):]
            ps_cmd.append(('%g %g o' % (x, y)))
    ps = '\n'.join(ps_cmd)
    self._draw_ps(ps, gc, rgbFace, fill=False, stroke=False)