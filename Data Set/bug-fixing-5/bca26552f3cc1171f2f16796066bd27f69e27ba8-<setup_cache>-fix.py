def setup_cache(self):
    if (not self.enabled):
        return {
            
        }
    with open(self.dump_fn, 'w') as f:
        json.dump({
            
        }, f, indent=2)