MOD = 998244353

def height(n, m):
    m %= MOD
    inv = [0] * (n + 1)
    last = 1
    ans = 0
    for i in range(1, n + 1):
        inv[i] = -(MOD // i) * inv[MOD % i] % MOD if i > 1 else 1
        last = last * (m - i + 1) * inv[i] % MOD
        ans = (ans + last) % MOD
    return ans
