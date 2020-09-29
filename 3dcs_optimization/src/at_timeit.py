import time

def timeit(func):
    def timed(*args, **kw):
        ts = time.time()
        result = func(*args, **kw)
        te = time.time()
        
        print('%r  %2.2f ms' % (func.__name__, (te - ts) * 1000))
        return result
    return timed