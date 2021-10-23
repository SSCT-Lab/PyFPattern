def use(self, styles):
    '\n        Set the styles on the current Styler, possibly using styles\n        from ``Styler.export``.\n\n        Parameters\n        ----------\n        styles : list\n            List of style functions.\n\n        Returns\n        -------\n        self : Styler\n\n        See Also\n        --------\n        Styler.export\n        '
    self._todo.extend(styles)
    return self