def v2_playbook_on_play_start(self, play):
    name = play.get_name().strip()
    if (not name):
        msg = 'PLAY'
    else:
        msg = ('PLAY [%s]' % name)
    self._display.banner(msg)