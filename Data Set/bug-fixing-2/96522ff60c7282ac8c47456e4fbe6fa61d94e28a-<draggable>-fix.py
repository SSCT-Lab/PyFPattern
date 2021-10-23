

def draggable(self, state=None, use_blit=False, update='loc'):
    '\n        Set the draggable state -- if state is\n\n          * None : toggle the current state\n\n          * True : turn draggable on\n\n          * False : turn draggable off\n\n        If draggable is on, you can drag the legend on the canvas with\n        the mouse. The `.DraggableLegend` helper instance is returned if\n        draggable is on.\n\n        The update parameter control which parameter of the legend changes\n        when dragged. If update is "loc", the *loc* parameter of the legend\n        is changed. If "bbox", the *bbox_to_anchor* parameter is changed.\n        '
    warn_deprecated('2.2', message='Legend.draggable() is deprecated in favor of Legend.set_draggable(). Legend.draggable may be reintroduced as a property in future releases.')
    if (state is None):
        state = (not self.get_draggable())
    self.set_draggable(state, use_blit, update)
    return self._draggable
