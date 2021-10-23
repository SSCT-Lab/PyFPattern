def _update_layout(self):
    '\n        Ask for a re computation of the application layout, if for example ,\n        some configuration options have changed.\n        '
    if getattr(self, '._app', None):
        self._app.layout = create_prompt_layout(**self._layout_options())