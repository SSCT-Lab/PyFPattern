def setup_cache(self):
    if (not self.enabled):
        return {
            
        }
    numtrials = slow
    results = {
        
    }
    solvers = ['DE', 'basinh.']
    for (name, klass) in sorted(self._functions.items()):
        try:
            f = klass()
            b = _BenchOptimizers.from_funcobj(name, f)
            with np.errstate(all='ignore'):
                b.bench_run_global(methods=solvers, numtrials=numtrials)
            results[name] = b.average_results()
        except:
            results[name] = '\n'.join(traceback.format_exc())
            continue
        dump_fn = os.path.join(os.path.dirname(__file__), '..', 'global-bench-results.json')
        with open(dump_fn, 'w') as f:
            json.dump(results, f, indent=2, sort_keys=True)
    return results