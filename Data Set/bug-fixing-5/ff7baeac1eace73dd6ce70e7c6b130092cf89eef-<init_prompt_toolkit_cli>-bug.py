def init_prompt_toolkit_cli(self):
    self._app = None
    if self.simple_prompt:

        def prompt():
            return cast_unicode_py2(input(('In [%d]: ' % self.execution_count)))
        self.prompt_for_code = prompt
        return
    kbmanager = KeyBindingManager.for_prompt()
    insert_mode = (ViInsertMode() | EmacsInsertMode())

    @kbmanager.registry.add_binding(Keys.ControlJ, filter=((HasFocus(DEFAULT_BUFFER) & (~ HasSelection())) & insert_mode))
    def _(event):
        b = event.current_buffer
        d = b.document
        if b.complete_state:
            cc = b.complete_state.current_completion
            if cc:
                b.apply_completion(cc)
            else:
                b.cancel_completion()
            return
        if (not (d.on_last_line or (d.cursor_position_row >= (d.line_count - d.empty_line_count_at_the_end())))):
            b.newline()
            return
        (status, indent) = self.input_splitter.check_complete((d.text + '\n'))
        if ((status != 'incomplete') and b.accept_action.is_returnable):
            b.accept_action.validate_and_handle(event.cli, b)
        else:
            b.insert_text(('\n' + (' ' * (indent or 0))))

    @kbmanager.registry.add_binding(Keys.ControlP, filter=(ViInsertMode() & HasFocus(DEFAULT_BUFFER)))
    def _previous_history_or_previous_completion(event):
        '\n            Control-P in vi edit mode on readline is history next, unlike default prompt toolkit.\n\n            If completer is open this still select previous completion.\n            '
        event.current_buffer.auto_up()

    @kbmanager.registry.add_binding(Keys.ControlN, filter=(ViInsertMode() & HasFocus(DEFAULT_BUFFER)))
    def _next_history_or_next_completion(event):
        '\n            Control-N in vi edit mode on readline is history previous, unlike default prompt toolkit.\n\n            If completer is open this still select next completion.\n            '
        event.current_buffer.auto_down()

    @kbmanager.registry.add_binding(Keys.ControlG, filter=(HasFocus(DEFAULT_BUFFER) & HasCompletions()))
    def _dismiss_completion(event):
        b = event.current_buffer
        if b.complete_state:
            b.cancel_completion()

    @kbmanager.registry.add_binding(Keys.ControlC, filter=HasFocus(DEFAULT_BUFFER))
    def _reset_buffer(event):
        b = event.current_buffer
        if b.complete_state:
            b.cancel_completion()
        else:
            b.reset()

    @kbmanager.registry.add_binding(Keys.ControlC, filter=HasFocus(SEARCH_BUFFER))
    def _reset_search_buffer(event):
        if event.current_buffer.document.text:
            event.current_buffer.reset()
        else:
            event.cli.push_focus(DEFAULT_BUFFER)
    supports_suspend = Condition((lambda cli: hasattr(signal, 'SIGTSTP')))

    @kbmanager.registry.add_binding(Keys.ControlZ, filter=supports_suspend)
    def _suspend_to_bg(event):
        event.cli.suspend_to_background()

    @Condition
    def cursor_in_leading_ws(cli):
        before = cli.application.buffer.document.current_line_before_cursor
        return ((not before) or before.isspace())

    @kbmanager.registry.add_binding(Keys.ControlI, filter=(((HasFocus(DEFAULT_BUFFER) & (~ HasSelection())) & insert_mode) & cursor_in_leading_ws))
    def _indent_buffer(event):
        event.current_buffer.insert_text((' ' * 4))
    if (self.display_completions == 'readlinelike'):

        @kbmanager.registry.add_binding(Keys.ControlI, filter=(((HasFocus(DEFAULT_BUFFER) & (~ HasSelection())) & insert_mode) & (~ cursor_in_leading_ws)))
        def _disaply_compl(ev):
            display_completions_like_readline(ev)
    if (sys.platform == 'win32'):
        from IPython.lib.clipboard import ClipboardEmpty, win32_clipboard_get, tkinter_clipboard_get

        @kbmanager.registry.add_binding(Keys.ControlV, filter=(HasFocus(DEFAULT_BUFFER) & (~ ViMode())))
        def _paste(event):
            try:
                text = win32_clipboard_get()
            except TryNext:
                try:
                    text = tkinter_clipboard_get()
                except (TryNext, ClipboardEmpty):
                    return
            except ClipboardEmpty:
                return
            event.current_buffer.insert_text(text.replace('\t', (' ' * 4)))
    history = InMemoryHistory()
    last_cell = ''
    for (__, ___, cell) in self.history_manager.get_tail(self.history_load_length, include_latest=True):
        cell = cell.rstrip()
        if (cell and (cell != last_cell)):
            history.append(cell)
    self._style = self._make_style_from_name(self.highlighting_style)
    style = DynamicStyle((lambda : self._style))
    editing_mode = getattr(EditingMode, self.editing_mode.upper())
    self._app = create_prompt_application(editing_mode=editing_mode, key_bindings_registry=kbmanager.registry, history=history, completer=IPythonPTCompleter(self.Completer), enable_history_search=True, style=style, mouse_support=self.mouse_support, **self._layout_options())
    self._eventloop = create_eventloop(self.inputhook)
    self.pt_cli = CommandLineInterface(self._app, eventloop=self._eventloop)