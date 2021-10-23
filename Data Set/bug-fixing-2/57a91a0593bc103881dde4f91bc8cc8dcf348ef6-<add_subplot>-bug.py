

def add_subplot(self, *args, **kwargs):
    "\n        Add a subplot.\n\n        Parameters\n        ----------\n        *args\n            Either a 3-digit integer or three separate integers\n            describing the position of the subplot. If the three\n            integers are I, J, and K in order, the subplot is the\n            Kth plot on a grid with I rows and J columns.\n\n        projection : ['aitoff' | 'hammer' | 'lambert' | 'mollweide' | 'polar' | 'rectilinear'], optional\n            The projection type of the axes.\n\n        polar : boolean, optional\n            If True, equivalent to projection='polar'.\n\n        **kwargs\n            This method also takes the keyword arguments for\n            :class:`~matplotlib.axes.Axes`.\n\n        Returns\n        -------\n        axes : Axes\n            The axes of the subplot.\n\n        Notes\n        -----\n        If the figure already has a subplot with key (*args*,\n        *kwargs*) then it will simply make that subplot current and\n        return it.  This behavior is deprecated.\n\n        Examples\n        --------\n        ::\n\n            fig.add_subplot(111)\n\n            # equivalent but more general\n            fig.add_subplot(1, 1, 1)\n\n            # add subplot with red background\n            fig.add_subplot(212, facecolor='r')\n\n            # add a polar subplot\n            fig.add_subplot(111, projection='polar')\n\n            # add Subplot instance sub\n            fig.add_subplot(sub)\n\n        See Also\n        --------\n        matplotlib.pyplot.subplot : for an explanation of the args.\n        "
    if (not len(args)):
        return
    if ((len(args) == 1) and isinstance(args[0], int)):
        if (not (100 <= args[0] <= 999)):
            raise ValueError('Integer subplot specification must be a three-digit number, not {}'.format(args[0]))
        args = tuple(map(int, str(args[0])))
    if isinstance(args[0], SubplotBase):
        a = args[0]
        if (a.get_figure() is not self):
            raise ValueError('The Subplot must have been created in the present figure')
        key = self._make_key(*args, **kwargs)
    else:
        (projection_class, kwargs, key) = process_projection_requirements(self, *args, **kwargs)
        ax = self._axstack.get(key)
        if (ax is not None):
            if isinstance(ax, projection_class):
                self.sca(ax)
                return ax
            else:
                self._axstack.remove(ax)
        a = subplot_class_factory(projection_class)(self, *args, **kwargs)
    self._axstack.add(key, a)
    self.sca(a)
    a._remove_method = self.__remove_ax
    self.stale = True
    a.stale_callback = _stale_figure_callback
    return a
