__import__('sys').setrecursionlimit(10000)


def square_sums(n):
    squares = [sq*sq for sq in range(2, int((n*2-1)**.5)+1)]
    Graph = {i: [j-i for j in squares if 0<j-i<=n and j-i!=i] for i in range(1, n+1)}
    
    def get_result(G, res, ind):
        if len(res) == n: return res
        
        for next_ind in sorted((G.keys() if ind == 0 else G[ind]),key=lambda x: len(G[x])):
        
            for i in G[next_ind]:
                G[i].remove(next_ind)
            res.append(next_ind)
            
            next_result = get_result(G, res, next_ind)
            if next_result != False: return next_result
            
            for i in G[next_ind]:
                G[i].append(next_ind)
            res.pop()
        
        return False
    
    return get_result(Graph, [], 0)
