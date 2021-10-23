def _start_frag_download(self, ctx):
    resume_len = ctx['complete_frags_downloaded_bytes']
    total_frags = ctx['total_frags']
    state = {
        'status': 'downloading',
        'downloaded_bytes': resume_len,
        'fragment_index': ctx['fragment_index'],
        'fragment_count': total_frags,
        'filename': ctx['filename'],
        'tmpfilename': ctx['tmpfilename'],
    }
    start = time.time()
    ctx.update({
        'started': start,
        'prev_frag_downloaded_bytes': 0,
    })

    def frag_progress_hook(s):
        if (s['status'] not in ('downloading', 'finished')):
            return
        time_now = time.time()
        state['elapsed'] = (time_now - start)
        frag_total_bytes = (s.get('total_bytes') or 0)
        if (not ctx['live']):
            estimated_size = (((ctx['complete_frags_downloaded_bytes'] + frag_total_bytes) / (state['fragment_index'] + 1)) * total_frags)
            state['total_bytes_estimate'] = estimated_size
        if (s['status'] == 'finished'):
            state['fragment_index'] += 1
            ctx['fragment_index'] = state['fragment_index']
            state['downloaded_bytes'] += (frag_total_bytes - ctx['prev_frag_downloaded_bytes'])
            ctx['complete_frags_downloaded_bytes'] = state['downloaded_bytes']
            ctx['prev_frag_downloaded_bytes'] = 0
        else:
            frag_downloaded_bytes = s['downloaded_bytes']
            state['downloaded_bytes'] += (frag_downloaded_bytes - ctx['prev_frag_downloaded_bytes'])
            if (not ctx['live']):
                state['eta'] = self.calc_eta(start, time_now, (estimated_size - resume_len), (state['downloaded_bytes'] - resume_len))
            state['speed'] = (s.get('speed') or ctx.get('speed'))
            ctx['speed'] = state['speed']
            ctx['prev_frag_downloaded_bytes'] = frag_downloaded_bytes
        self._hook_progress(state)
    ctx['dl'].add_progress_hook(frag_progress_hook)
    return start