def add_widget(self, widget, index=0, canvas=None):
    "Add a new widget as a child of this widget.\n\n        :Parameters:\n            `widget`: :class:`Widget`\n                Widget to add to our list of children.\n            `index`: int, defaults to 0\n                Index to insert the widget in the list. Notice that the default\n                of 0 means the widget is inserted at the beginning of the list\n                and will thus be drawn on top of other sibling widgets. For a\n                full discussion of the index and widget hierarchy, please see\n                the :doc:`Widgets Programming Guide <guide/widgets>`.\n\n                .. versionadded:: 1.0.5\n            `canvas`: str, defaults to None\n                Canvas to add widget's canvas to. Can be 'before', 'after' or\n                None for the default canvas.\n\n                .. versionadded:: 1.9.0\n\n    .. code-block:: python\n\n        >>> from kivy.uix.button import Button\n        >>> from kivy.uix.slider import Slider\n        >>> root = Widget()\n        >>> root.add_widget(Button())\n        >>> slider = Slider()\n        >>> root.add_widget(slider)\n\n        "
    if (not isinstance(widget, Widget)):
        raise WidgetException('add_widget() can be used only with instances of the Widget class.')
    widget = widget.__self__
    if (widget is self):
        raise WidgetException('Widget instances cannot be added to themselves.')
    parent = widget.parent
    if parent:
        raise WidgetException(('Cannot add %r, it already has a parent %r' % (widget, parent)))
    widget.parent = parent = self
    if parent.disabled:
        widget.disabled = True
    canvas = (self.canvas.before if (canvas == 'before') else (self.canvas.after if (canvas == 'after') else self.canvas))
    if ((index == 0) or (len(self.children) == 0)):
        self.children.insert(0, widget)
        canvas.add(widget.canvas)
    else:
        canvas = self.canvas
        children = self.children
        if (index >= len(children)):
            index = len(children)
            next_index = canvas.indexof(children[(- 1)].canvas)
        else:
            next_child = children[index]
            next_index = canvas.indexof(next_child.canvas)
            if (next_index == (- 1)):
                next_index = canvas.length()
            else:
                next_index += 1
        children.insert(index, widget)
        if ((next_index == 0) and canvas.has_before):
            next_index = 1
        canvas.insert(next_index, widget.canvas)