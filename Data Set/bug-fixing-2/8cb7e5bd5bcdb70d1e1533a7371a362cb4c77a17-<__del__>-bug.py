

def __del__(self):
    if ((self.__misses != 0) and (self.__hits == 0)):
        warnings.warn('{} was marked with JIT and invoked {} times, but we never successfully used compiled code.'.format(repr(self), self.__hits))
    if _JIT_STATS:
        print('{} - hits: {}, misses: {}, cache_size: {}'.format(repr(self), self.__hits, self.__misses, len(self.__ktrace_cache)))
