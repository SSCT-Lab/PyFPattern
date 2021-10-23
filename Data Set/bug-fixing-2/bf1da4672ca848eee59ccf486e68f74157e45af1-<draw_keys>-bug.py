

def draw_keys(self):
    layout = self.available_layouts[self.layout]
    layout_rows = layout['rows']
    layout_geometry = self.layout_geometry
    layout_mode = self.layout_mode
    (w, h) = self.size
    background = resource_find((self.background_disabled if self.disabled else self.background))
    texture = Image(background, mipmap=True).texture
    self.background_key_layer.clear()
    with self.background_key_layer:
        Color(*self.background_color)
        BorderImage(texture=texture, size=self.size, border=self.background_border)
    key_normal = resource_find((self.key_background_disabled_normal if self.disabled else self.key_background_normal))
    texture = Image(key_normal, mipmap=True).texture
    with self.background_key_layer:
        for line_nb in range(1, (layout_rows + 1)):
            for (pos, size) in layout_geometry[('LINE_%d' % line_nb)]:
                BorderImage(texture=texture, pos=pos, size=size, border=self.key_border)
    font_size = (int(w) / 46)
    for line_nb in range(1, (layout_rows + 1)):
        key_nb = 0
        for (pos, size) in layout_geometry[('LINE_%d' % line_nb)]:
            text = layout[((layout_mode + '_') + str(line_nb))][key_nb][0]
            z = Label(text=text, font_size=font_size, pos=pos, size=size, font_name=self.font_name)
            self.add_widget(z)
            key_nb += 1
