N = 7
perms = {i:set() for i in range(0, N+1)}
for row in __import__('itertools').permutations(range(1,N+1), N):
    c, s = 0, 0
    for h in row:
        if h>c: c, s = h, s+1
    perms[0].add(row)
    perms[s].add(row)

def solve_puzzle (clues):
    rows = [perms[r]&{p[::-1] for p in perms[l]} for (r, l) in zip(clues[N*4-1:N*3-1:-1],clues[N:N*2])]
    cols = [perms[t]&{p[::-1] for p in perms[b]} for (t, b) in zip(clues[0:N],clues[N*3-1:N*2-1:-1])]
    
    for _ in range(N*N//2):
        for r_i in range(N):
            for c_i in range(N):
                common = {r[c_i] for r in rows[r_i]} & {c[r_i] for c in cols[c_i]}
                rows[r_i], cols[c_i] = [r for r in rows[r_i] if r[c_i] in common], [c for c in cols[c_i] if c[r_i] in common]
    
    for rows1 in __import__('itertools').product(*rows):
        if all(tuple(r[i] for r in rows1) in cols[i] for i in range(N)): return list(list(r) for r in rows1)
