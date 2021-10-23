def execute(self, query, params=None):
    if (query.upper().strip('; ') == 'VACUUM'):
        self.db.commit('vacuum called')
    query = query.strip()
    while self.db.progress_sleeping:
        time.sleep(0.1)
    self.db.last_query_time = time.time()
    (query, params) = self.parseQuery(query, params)
    s = time.time()
    try:
        self.lock.acquire(True)
        if params:
            res = self.cursor.execute(query, params)
            if self.logging:
                self.db.log.debug((((query + ' ') + str(params)) + (' (Done in %.4f)' % (time.time() - s))))
        else:
            res = self.cursor.execute(query)
            if self.logging:
                self.db.log.debug((query + (' (Done in %.4f)' % (time.time() - s))))
    finally:
        self.lock.release()
    if self.db.collect_stats:
        if (query not in self.db.query_stats):
            self.db.query_stats[query] = {
                'call': 0,
                'time': 0.0,
            }
        self.db.query_stats[query]['call'] += 1
        self.db.query_stats[query]['time'] += (time.time() - s)
    if (not self.db.need_commit):
        query_type = query.split(' ', 1)[0].upper()
        if (query_type in ['UPDATE', 'DELETE', 'INSERT', 'CREATE']):
            self.db.need_commit = True
    return res