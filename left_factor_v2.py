def lcs(X, Y,m,n):
    if m == 0 or n == 0:
       return 0;
    elif X[m-1] == Y[n-1]:
       return 1 + lcs(X, Y, m-1, n-1);
    else:
       return max(lcs(X, Y, m, n-1), lcs(X, Y, m-1, n));

def left_factor(grammar):
    smallest_prod = ""

    for key,item in grammar.copy().items():
        x = 0
        if len(item) == 1:
            continue
        smallest_prod = min(item,key=lambda x: len(x))
        min_len = len(smallest_prod)
        
        for prod in item:
            if prod == smallest_prod: continue
            x = lcs(prod , smallest_prod,len(prod),len(smallest_prod))
            if min_len>= x:
                min_len = x
        
        if x>0:
            grammar[key+"'"] = []
            for p in item:
                fac=p[0:min_len]
                grammar[key+"'"].append(p[min_len:] if p[min_len:] else 'ε')
            grammar.update({key:[fac+key+"'"]})

    return grammar


if __name__=="__main__":
    # grammar = {'S': ['iEtSeS', 'iEtS'], 'E': ['b']}
    
    grammar = {'E': ["TE'"], 'T': ["FT'"], 'F': ['(E)', 'i'], "E'": ['ε', "+TE'"], "T'": ['ε', "*FT'"]}
    start = 'E'
    print ("the given grammar grammar\n",grammar)
    print ("left factoring grammar")
    print(left_factor(grammar))