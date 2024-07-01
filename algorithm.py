def Reverse(s):
    return s[::-1]


def findR(Vn, str0, grammar):
    if Vn in grammar.keys():
        ProRight = grammar[Vn]
        for prod in ProRight:
            if str0 == prod[0]:
                return prod
    return ''


def findL(item, grammar):
    for SL in grammar.keys():
        for it in grammar[SL]:
            if it == item:
                return SL
    return ''


def addS(V, S):
    newS = list(S)
    for i in V:
        newS.append(i)
    return newS


def Fi(S, grammar, VN, VT):
    if S in VN:
        Fi = []
        return First(S, Fi, grammar, VN, VT)
    else:
        return list(S)


def First(S, Fi, grammar, VN, VT):
    if S in grammar:
        # print("grammer: ", grammar)
        for item in grammar[S]:
            if item[0] in VT or item[0] == 'ε':
                Fi.append(item[0])
            else:
                First(item[0], Fi, grammar, VN, VT)
    Fi = list(set(Fi))
    Fi.sort()
    return Fi


def Fo(S, grammar, VN, VT):
    if S in VN:
        Fo = []
        Fo = Follow(S, Fo, grammar, VN, VT)
        Fo = list(set(Fo))
        Fo.sort()
        if 'ε' in Fo:
            Fo.remove('ε')
        return Fo
    else:
        return list(S)


def Follow(S, Fo, grammar, VN, VT):
    if S == VN[0]:
        Fo.append('#')
    for A in grammar:
        for item in grammar[A]:
            for i, symbol in enumerate(item):
                if symbol == S:
                    if i + 1 < len(item):
                        next_symbol = item[i + 1]
                        if next_symbol in VT:
                            Fo.append(next_symbol)
                        else:
                            first_next = Fi(next_symbol, grammar, VN, VT)
                            if 'ε' in first_next:
                                first_next.remove('ε')
                                Fo.extend(first_next)
                                if A != S:
                                    Fo.extend(Follow(A, [], grammar, VN, VT))
                            else:
                                Fo.extend(first_next)
                    else:
                        if A != S:
                            Fo.extend(Follow(A, [], grammar, VN, VT))
    return list(set(Fo))


def Se(S, V, VN, VT, grammar):
    if S in VN:
        Se = []
        return Select(S, V, Se, VN, VT, grammar)


def Select(S, V, Se, VN, VT, grammar):
    if V[0] in VT and V[0] != 'ε':
        return list(V[0])
    elif V[0] == 'ε':
        Se.extend(Fo(S, grammar, VN, VT))
        return Se
    elif V[0] in VN:
        if 'ε' in grammar[V[0]]:
            Se.extend(V[1:])
            if 'ε' in Se:
                Se.remove('ε')
            Se.extend(Fo(V[0], grammar, VN, VT))
        Se.extend(Fi(V[0], grammar, VN, VT))
        return Se
    return Se


def is_LL1(grammar, VN, VT, select_dict):
    first = {vn: Fi(vn, grammar, VN, VT) for vn in VN}
    follow = {vn: Fo(vn, grammar, VN, VT) for vn in VN}
    select = select_dict
    analysis_table = {vn: {vt: '' for vt in VT + ['#']} for vn in VN}
    is_ll1 = True
    print("first: ", first)
    print("follow：", follow)
    print("select: ", select)
    print(analysis_table)

    for nt in VN:
        select_sets = []
        for prod in grammar[nt]:
            select_sets.append(set(Se(nt, prod, VN, VT, grammar)))
        for i in range(len(select_sets)):
            for j in range(i + 1, len(select_sets)):
                if select_sets[i].intersection(select_sets[j]):
                    is_ll1 = False

    return is_ll1, first, follow, select, analysis_table


