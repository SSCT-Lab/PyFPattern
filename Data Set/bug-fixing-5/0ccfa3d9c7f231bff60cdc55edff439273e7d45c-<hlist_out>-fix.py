def hlist_out(self, box):
    cur_g = 0
    cur_glue = 0.0
    glue_order = box.glue_order
    glue_sign = box.glue_sign
    base_line = self.cur_v
    left_edge = self.cur_h
    self.cur_s += 1
    self.max_push = max(self.cur_s, self.max_push)
    clamp = self.clamp
    for p in box.children:
        if isinstance(p, Char):
            p.render((self.cur_h + self.off_h), (self.cur_v + self.off_v))
            self.cur_h += p.width
        elif isinstance(p, Kern):
            self.cur_h += p.width
        elif isinstance(p, List):
            if (len(p.children) == 0):
                self.cur_h += p.width
            else:
                edge = self.cur_h
                self.cur_v = (base_line + p.shift_amount)
                if isinstance(p, Hlist):
                    self.hlist_out(p)
                else:
                    self.vlist_out(p)
                self.cur_h = (edge + p.width)
                self.cur_v = base_line
        elif isinstance(p, Box):
            rule_height = p.height
            rule_depth = p.depth
            rule_width = p.width
            if isinf(rule_height):
                rule_height = box.height
            if isinf(rule_depth):
                rule_depth = box.depth
            if ((rule_height > 0) and (rule_width > 0)):
                self.cur_v = (base_line + rule_depth)
                p.render((self.cur_h + self.off_h), (self.cur_v + self.off_v), rule_width, rule_height)
                self.cur_v = base_line
            self.cur_h += rule_width
        elif isinstance(p, Glue):
            glue_spec = p.glue_spec
            rule_width = (glue_spec.width - cur_g)
            if (glue_sign != 0):
                if (glue_sign == 1):
                    if (glue_spec.stretch_order == glue_order):
                        cur_glue += glue_spec.stretch
                        cur_g = np.round(clamp((float(box.glue_set) * cur_glue)))
                elif (glue_spec.shrink_order == glue_order):
                    cur_glue += glue_spec.shrink
                    cur_g = np.round(clamp((float(box.glue_set) * cur_glue)))
            rule_width += cur_g
            self.cur_h += rule_width
    self.cur_s -= 1