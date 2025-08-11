def get_clashes(timings: dict) -> dict:
    from collections import defaultdict
    clashes = defaultdict(set)
    secs = list(timings.keys())

    for i, s1 in enumerate(secs):
        for s2 in secs[i+1:]:
            t1, t2 = timings[s1], timings[s2]
            if any(d1 == d2 and st1 == st2 for d1, st1, _ in t1 for d2, st2, _ in t2):
                clashes[s1].add(s2)
                clashes[s2].add(s1)
    return dict(clashes)