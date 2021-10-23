def finalize_offset(self):
    if (self._update == 'loc'):
        self._update_loc(self.get_loc_in_canvas())
    elif (self._update == 'bbox'):
        self._bbox_to_anchor(self.get_loc_in_canvas())