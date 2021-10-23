

@Pyro4.expose
def getstate(self):
    '\n        Merge projections from across all workers and return the final projection.\n        '
    logger.info('end of input, assigning all remaining jobs')
    logger.debug('jobs done: %s, jobs received: %s', self._jobsdone, self._jobsreceived)
    while (self._jobsdone < self._jobsreceived):
        time.sleep(0.5)
    logger.info('merging states from %i workers', len(self.workers))
    workers = list(self.workers.items())
    result = workers[0][1].getstate()
    for (workerid, worker) in workers[1:]:
        logger.info('pulling state from worker %s', workerid)
        result.merge(worker.getstate())
    logger.info('sending out merged projection')
    return result
