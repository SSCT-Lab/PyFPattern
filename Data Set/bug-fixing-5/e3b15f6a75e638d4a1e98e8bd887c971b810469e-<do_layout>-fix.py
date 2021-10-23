def do_layout(self, *largs):
    if (not self.children):
        self.minimum_size = (0.0, 0.0)
        return
    selfpos = self.pos
    selfsize = self.size
    orientation = self.orientation.split('-')
    padding_left = self.padding[0]
    padding_top = self.padding[1]
    padding_right = self.padding[2]
    padding_bottom = self.padding[3]
    padding_x = (padding_left + padding_right)
    padding_y = (padding_top + padding_bottom)
    (spacing_x, spacing_y) = self.spacing
    posattr = ([0] * 2)
    posdelta = ([0] * 2)
    posstart = ([0] * 2)
    for i in (0, 1):
        posattr[i] = (1 * (orientation[i] in ('tb', 'bt')))
        k = posattr[i]
        if (orientation[i] == 'lr'):
            posdelta[i] = 1
            posstart[i] = (selfpos[k] + padding_left)
        elif (orientation[i] == 'bt'):
            posdelta[i] = 1
            posstart[i] = (selfpos[k] + padding_bottom)
        elif (orientation[i] == 'rl'):
            posdelta[i] = (- 1)
            posstart[i] = ((selfpos[k] + selfsize[k]) - padding_right)
        else:
            posdelta[i] = (- 1)
            posstart[i] = ((selfpos[k] + selfsize[k]) - padding_top)
    (innerattr, outerattr) = posattr
    (ustart, vstart) = posstart
    (deltau, deltav) = posdelta
    del posattr, posdelta, posstart
    u = ustart
    v = vstart
    if (orientation[0] in ('lr', 'rl')):
        sv = padding_y
        su = padding_x
        spacing_u = spacing_x
        spacing_v = spacing_y
        padding_u = padding_x
        padding_v = padding_y
    else:
        sv = padding_x
        su = padding_y
        spacing_u = spacing_y
        spacing_v = spacing_x
        padding_u = padding_y
        padding_v = padding_x
    lv = 0
    urev = (deltau < 0)
    vrev = (deltav < 0)
    firstchild = self.children[0]
    sizes = []
    lc = []
    for c in reversed(self.children):
        if (c.size_hint[outerattr] is not None):
            c.size[outerattr] = max(1, _compute_size(c, (selfsize[outerattr] - padding_v), outerattr))
        ccount = len(lc)
        totalsize = availsize = max(0, ((selfsize[innerattr] - padding_u) - (spacing_u * ccount)))
        if (not lc):
            if (c.size_hint[innerattr] is not None):
                childsize = max(1, _compute_size(c, totalsize, innerattr))
            else:
                childsize = max(0, c.size[innerattr])
            availsize = ((selfsize[innerattr] - padding_u) - childsize)
            testsizes = [childsize]
        else:
            testsizes = ([0] * (ccount + 1))
            for (i, child) in enumerate(lc):
                if (availsize <= 0):
                    availsize = (- 1)
                    break
                if (child.size_hint[innerattr] is not None):
                    testsizes[i] = childsize = max(1, _compute_size(child, totalsize, innerattr))
                else:
                    testsizes[i] = childsize = max(0, child.size[innerattr])
                availsize -= childsize
            if (c.size_hint[innerattr] is not None):
                testsizes[(- 1)] = max(1, _compute_size(c, totalsize, innerattr))
            else:
                testsizes[(- 1)] = max(0, c.size[innerattr])
            availsize -= testsizes[(- 1)]
        if (((availsize + 1e-10) >= 0) or (not lc)):
            lc.append(c)
            sizes = testsizes
            lv = max(lv, c.size[outerattr])
            continue
        for (i, child) in enumerate(lc):
            if (child.size_hint[innerattr] is not None):
                child.size[innerattr] = sizes[i]
        sv += (lv + spacing_v)
        for c2 in lc:
            if urev:
                u -= c2.size[innerattr]
            c2.pos[innerattr] = u
            pos_outer = v
            if vrev:
                pos_outer -= c2.size[outerattr]
            c2.pos[outerattr] = pos_outer
            if urev:
                u -= spacing_u
            else:
                u += (c2.size[innerattr] + spacing_u)
        v += (deltav * lv)
        v += (deltav * spacing_v)
        lc = [c]
        lv = c.size[outerattr]
        if (c.size_hint[innerattr] is not None):
            sizes = [max(1, _compute_size(c, (selfsize[innerattr] - padding_u), innerattr))]
        else:
            sizes = [max(0, c.size[innerattr])]
        u = ustart
    if lc:
        for (i, child) in enumerate(lc):
            if (child.size_hint[innerattr] is not None):
                child.size[innerattr] = sizes[i]
        sv += (lv + spacing_v)
        for c2 in lc:
            if urev:
                u -= c2.size[innerattr]
            c2.pos[innerattr] = u
            pos_outer = v
            if vrev:
                pos_outer -= c2.size[outerattr]
            c2.pos[outerattr] = pos_outer
            if urev:
                u -= spacing_u
            else:
                u += (c2.size[innerattr] + spacing_u)
    self.minimum_size[outerattr] = sv