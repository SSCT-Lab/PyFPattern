

def play(self):
    if (self._ffplayer and (self._state == 'paused')):
        self._ffplayer.toggle_pause()
        self._state = 'playing'
        return
    self.load()
    self._out_fmt = 'rgba'
    ff_opts = {
        'paused': True,
        'out_fmt': self._out_fmt,
        'sn': True,
        'volume': self._volume,
    }
    self._ffplayer = MediaPlayer(self._filename, callback=self._player_callback, thread_lib='SDL', loglevel='info', ff_opts=ff_opts)
    self._thread = Thread(target=self._next_frame_run, name='Next frame')
    self._thread.daemon = True
    self._thread.start()
