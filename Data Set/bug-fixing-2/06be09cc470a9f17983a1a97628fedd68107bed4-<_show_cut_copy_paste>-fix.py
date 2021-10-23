

def _show_cut_copy_paste(self, pos, win, parent_changed=False, mode='', pos_in_window=False, *l):
    if (not self.use_bubble):
        return
    bubble = self._bubble
    if (bubble is None):
        self._bubble = bubble = TextInputCutCopyPaste(textinput=self)
        self.fbind('parent', self._show_cut_copy_paste, pos, win, True)
        self.bind(focus=(lambda *args: self._hide_cut_copy_paste(win)))
        self.bind(cursor_pos=(lambda *args: self._hide_cut_copy_paste(win)))
    else:
        win.remove_widget(bubble)
        if (not self.parent):
            return
    if parent_changed:
        return
    (lh, ls) = (self.line_height, self.line_spacing)
    (x, y) = pos
    t_pos = ((x, y) if pos_in_window else self.to_window(x, y))
    bubble_size = bubble.size
    bubble_hw = (bubble_size[0] / 2.0)
    win_size = win.size
    bubble_pos = (t_pos[0], (t_pos[1] + inch(0.25)))
    if ((bubble_pos[0] - bubble_hw) < 0):
        if (bubble_pos[1] > (win_size[1] - bubble_size[1])):
            bubble_pos = (bubble_hw, (t_pos[1] - ((lh + ls) + inch(0.25))))
            bubble.arrow_pos = 'top_left'
        else:
            bubble_pos = (bubble_hw, bubble_pos[1])
            bubble.arrow_pos = 'bottom_left'
    elif ((bubble_pos[0] + bubble_hw) > win_size[0]):
        if (bubble_pos[1] > (win_size[1] - bubble_size[1])):
            bubble_pos = ((win_size[0] - bubble_hw), (t_pos[1] - ((lh + ls) + inch(0.25))))
            bubble.arrow_pos = 'top_right'
        else:
            bubble_pos = ((win_size[0] - bubble_hw), bubble_pos[1])
            bubble.arrow_pos = 'bottom_right'
    elif (bubble_pos[1] > (win_size[1] - bubble_size[1])):
        bubble_pos = (bubble_pos[0], (t_pos[1] - ((lh + ls) + inch(0.25))))
        bubble.arrow_pos = 'top_mid'
    else:
        bubble.arrow_pos = 'bottom_mid'
    bubble_pos = self.to_widget(*bubble_pos, relative=True)
    bubble.center_x = bubble_pos[0]
    if (bubble.arrow_pos[0] == 't'):
        bubble.top = bubble_pos[1]
    else:
        bubble.y = bubble_pos[1]
    bubble.mode = mode
    Animation.cancel_all(bubble)
    bubble.opacity = 0
    win.add_widget(bubble, canvas='after')
    Animation(opacity=1, d=0.225).start(bubble)
