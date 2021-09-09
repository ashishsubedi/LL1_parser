from copy import deepcopy

def first(grammar, term):
    a = []
    if term not in grammar:
        return [term]

    for prod in grammar[term]:
        if prod[0] not in grammar:
            a.append(prod[0])
        elif prod[0] in grammar:
            a += first(grammar, prod[0])
    return a




def fo(grammar,start,terminals, non_terminals,firsts):

    follows = {}
    follows_set = {}

    # Make sure every production is one letter, do that by replacing ' prods with other letters
    for i in grammar:
        follows_set[i] = False
        if i == start:
            follows[i] = ['$']
        else:
            follows[i] = []

    prev_follows = {}
    while True:
        if prev_follows == follows:
            break
        else:
            prev_follows = deepcopy(follows)

        for key in non_terminals:
            for rule,prods in grammar.items():
                for prod in prods:
                    if key in prod:
                        idx = prod.index(key)
                        if idx+1 != len(prod):
                            if 'ε' == prod[idx+1]:
                                continue
                                # follows[key] += follows[char]
                                # follows[key] = list(set(follows[key]))
                            elif prod[idx+1] in terminals:
                                follows[key] += prod[idx+1]
                                follows[key] = list(set(follows[key]))
                                follows_set[key] = True
                            else:

                                follows[key] += firsts[prod[idx+1]]
                                follows[key] = list(set(follows[key]) - set('ε'))
                                follows_set[key] = True



                        else:
                            if key == rule:
                                continue
                            if follows_set[rule]:
                                follows[key] += follows[rule]
                                follows[key] = list(set(follows[key]))
                                follows_set[key] = True

    

    return follows

def parse_table(result,firsts,follows,terminals, augmentation={}):
    resMod = deepcopy(result)

    # create predictive parsing table
    tterm = list(terminals)
    if 'ε' in tterm:
        tterm.pop(tterm.index('ε' ))
    tterm += ["$"]
    M = {}
    for rule,prods in resMod.items():
        for prod in prods:
            if prod[0] in tterm:
                if M.get((rule,prod[0])) is None: 
                    M[(rule,prod[0])] = []
                M[(rule,prod[0])] += [prod]
            elif 'ε' in prod[0]:
                for a in follows[rule]:
                    if M.get((rule,a)) is None: M[((rule,a))] = []
                    M[(rule,a)] += [prod]
            else:
                for a in firsts[prod[0]]:
                    if 'ε' == a:
                        for b in follows[rule]:
                            if M.get((rule,b)) is None: M[((rule,b))] = []

                            M[(rule,b)] += [prod]
                    else:
                        if M.get((rule,a)) is None: M[((rule,a))] = []

                        M[(rule,a)] += [prod]
    # print(M)
    toprint = f'{"": <10}'
    for i in tterm:
        k = i
        
        for key,val in augmentation.items():
            if val == i:

                k  = key
        toprint += f'|{k: <10}'
    print(toprint)
    for i in result:
        k = i
        
        for key,val in augmentation.items():
            if val == i:

                k  = key
        toprint = f'{k: <10}'
        for j in tterm:
            if M.get((i,j)):
                values = ''
                for val in M[(i,j)]:        
                    for key,valu in augmentation.items():
                        if valu in val:
                           val = val.replace(valu,key)

                    values += f'{val} |'

                values = values[:-1]
                
                k = i
        
                for key,val in augmentation.items():
                    if val == i:

                        k  = key
                toprint += f'|{k+"->"+values: <10}' 
            else:
                # values = f'{val},'for val in M[(i,j)]

                toprint += f'|{M.get((i,j),"") : <10}'
        print(f'{"-":-<76}')
        print(toprint)
    return M

def parse(user_input,start_symbol,parsingTable):

    #flag
    flag = 0

    #appending dollar to end of input
    user_input = user_input + "$"

    stack = []

    stack.append("$")
    stack.append(start_symbol)

    input_len = len(user_input)
    index = 0

    print()
    print(f'{"Stack": <15}'+"|"+f'{"Input Buffer": <15}'+"|"+f'Output')
    print(f'{"-":-<50}')
    stack_str = "".join(stack)
    print(f'{stack_str: <15}'+"|"+f'{user_input[index:]: <15}'+"|"+f'')
    while len(stack) > 1:

        # print(stack)

        #element at top of stack
        top = stack[-1]
        #print("Top =>", top)
        #current input
        current_input = user_input[index]

        # print("Current_Input => ",current_input)

        if top == current_input:
            stack.pop()
            index = index + 1	
            stack_str = "".join(stack)
            print(f'{stack_str: <15}'+"|"+f'{user_input[index:]: <15}'+"|"+f'Match {current_input}')
            continue
        else:	

            #finding value for key in table
            key = (top , current_input)
         #   print(key)

        #top of stack terminal => not accepted
        if key not in parsingTable:
            flag = 1	
            stack_str = "".join(stack)
            print(f'{stack_str: <15}'+"|"+f'{user_input[index:]: <15}'+"|"+f'Rejected')

            break

        value = parsingTable[key]
        rule = value

        if value != ['ε']:
            value = [sub_x for x in value for sub_x in x]
            value = value[::-1]
            #poping top of stack
            stack.pop()

            #push value chars to stack
            for element in value:
                stack.append(element)
            stack_str = "".join(stack)
            print(f'{stack_str: <15}'+"|"+f'{user_input[index:]: <15}'+"|"+f'{key[0]} -> {rule[0]}')
            
        else:
            stack.pop()	

    if flag== 0:
        print("Accepted")
    else:
        print("Rejected")

if __name__ == "__main__":

    start = 'S'
    # grammar = {'S': ["iEtSS'"], 'E': ['b'], "S'": ['eS', 'ε']}
    grammar = {'S': ["iEtSY"], "Y": ['eY', 'ε'], 'E': ['b']}
    # {'E': ['TX'], 'X': ['E', 'e'], 'T': ['F', 'Y'], 'Y': ['T', 'e'], 'F': ['PZ'], 'Z': ['*Z', 'e'], 'P': ['(E)', 'a', 'b', 'e']}


    # result = rem(grammar)
    result = grammar
    terminals = []
    for i in result:
        for j in result[i]:
            for k in j:
                if k not in result:
                    terminals += [k]

    terminals = list(set(terminals) - {"'"})

    non_terminals = set(result.keys())

    firsts = {}

    for i in result:
        firsts[i] = first(result, i)
        print(f'First({i}):', firsts[i])

    follows = fo(result,start,terminals, non_terminals,firsts)
    for i in result:
        firsts[i] = first(result, i)
        print(f'Follow({i}):', follows[i])
    # print (follows)
    # follow_v2(grammar,'S',terminals,firsts)
    # for terminal in terminals:
    #     follow_grammar = follow_v2(grammar,terminal,firsts,'S')
    #     print(follow_grammar)


    

    # predective_parse(result)
    M = parse_table(result,firsts,follows,terminals)

    # parse_string("ibtibt",M,terminals, non_terminals)
    # parse_string('ibtibt',grammar,start)
    parse('ibtibt',start,M)
