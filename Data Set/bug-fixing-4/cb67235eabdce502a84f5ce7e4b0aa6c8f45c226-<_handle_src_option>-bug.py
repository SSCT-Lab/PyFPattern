def _handle_src_option(self):
    try:
        self._handle_template()
    except ValueError as exc:
        return dict(failed=True, msg=to_text(exc))