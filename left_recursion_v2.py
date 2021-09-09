def left_recursion(grammar):


    for key,item in grammar.copy().items():
        recursive = []
        non_recursive = []

        for prod in item:
            if key == prod[0]:
                recursive.append(prod)
            else:
                non_recursive.append(prod)
        if not recursive:
            continue
        for i in range(len(non_recursive)):
            non_recursive[i] += key+"'"

        grammar[key] = non_recursive
        grammar[key+"'"] = ['ε']

        for i in range(len(recursive)):
            subfix = recursive[i][1:]
            grammar.update({key+"'": grammar[key+"'"]+[subfix+key+"'"]})

    return grammar


if __name__ == "__main__":
    grammar = {}
    lis = list()
    # le = input("length")
    # for i in range(0,le):
    # 	key = raw_input("key")
    # 	l = input("number of production")
    # 	lis = list()
    # 	for i in range(0,l):
    # 		lis.append(raw_input())
    # 	grammar.update({key:lis})
    #grammar = {"S":["abAB","abc","abcdA"],"A":["d","psln"],"B":["e","psln"]}
    grammar = {"E": ["E+T", "T", "EabcdA"]}
    # grammar = {'S ': [' iEtSeS ', ' iEtS'], 'E': ['b']}
    print("the given grammar grammar\n", grammar)
    print("removing left recursion free grammar")
    print(left_recursion(grammar))
