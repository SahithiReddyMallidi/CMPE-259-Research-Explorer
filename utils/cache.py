from functools import lru_cache

@lru_cache(maxsize=1000)
def cached_answer(q):
    return q
