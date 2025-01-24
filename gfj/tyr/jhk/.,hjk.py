def loopover(mixed, solved):
    t = {c: (i, j) for (i, row) in enumerate(solved) for (j, c) in enumerate(row)}
    b = {(i, j): t[c] for (i, row) in enumerate(mixed) for j, c in enumerate(row)}
    unsolved = {k for k, v in b.items() if k not in ((0, 0), (0, 1)) and k != v}
    sol = []

    while unsolved:
        i, j = next(iter(unsolved)) if b[0, 0] in ((0, 0), (0, 1)) else b[0, 0]
        if i == 0:
            sol += [f"D{j}", *j * ["L1"], "L0", "U0", "R0", "D0", *j * ["R1"], f"U{j}"]
        else:
            sol += [*j * [f"L{i}"], "L0", *i * ["U0"], "R0", *i * ["D0"], *j * [f"R{i}"]]
        b[0, 0], b[0, 1], b[i, j] = b[0, 1], b[i, j], b[0, 0]

        if b[i, j] == (i, j):
            unsolved.remove((i, j))

    if b[0, 0] != (0, 0) and len(mixed) % 2 == 0:
        sol += [*len(mixed) // 2 * ["D0", "L0", "D0", "R0"], "D0"]
    elif b[0, 0] != (0, 0) and len(mixed[0]) % 2 == 0:
        sol += [*len(mixed[0]) // 2 * ["R0", "U0", "R0", "D0"], "U0", "R0", "D0"]
    elif b[0, 0] != (0, 0):
        return None

    return sol
