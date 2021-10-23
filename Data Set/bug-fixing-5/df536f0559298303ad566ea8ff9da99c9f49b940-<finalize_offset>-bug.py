def finalize_offset(self):
    update_method = cbook._check_getitem({
        'loc': self._update_loc,
        'bbox': self._bbox_to_anchor,
    }, update=self._update)
    update_method(self.get_loc_in_canvas())