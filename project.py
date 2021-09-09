from utils import add_to_grammar, format_output
from left_recursion_v2 import left_recursion
from left_factor_v2 import left_factor
from predective_parser import first, fo, parse_table, parse

replacements = ['U','V','W','X','Y','Z']

if __name__ == "__main__":
    n = int(input("Enter No of Production: "))
    for i in range(n):
        txt=input()
        grammar = add_to_grammar(txt)
    start = input("Start")

    print(grammar)

    result = left_recursion(grammar)
    print()
    print("After Elimination of left recursion:")
    print()
    for x,y in result.items():
        print(f'{x} -> {format_output(y)}')

    result = left_factor(grammar)
    print()
    print("After Left Factoring:")
    for x,y in result.items():
        print(f'{x} -> {format_output(y)}')
    print()

    augmentation = {}
    for rule in result:
        if "'" in rule:
            augmentation[rule] = replacements.pop()
    new_result = {}

    for rule,prods in result.items():
        if rule in augmentation:
            key = augmentation[rule]
        else:
            key = rule
        new_result[key] = []
        for prod in prods:
            for (aug_key,aug_val) in augmentation.items():
                prod = prod.replace(aug_key,aug_val)    
            new_result[key].append(prod) 


    result = new_result.copy()

    print()

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
        firsts[i] = list(set(first(result, i)))
        k = i
        for key,val in augmentation.items():
            if val == i:

                k  = key
        
        print(f'First({k}):', firsts[i])
    print()

    follows = fo(result,start,terminals, non_terminals,firsts)
    for i in result:
        firsts[i] = first(result, i)
        
        k = i
        for key,val in augmentation.items():
            if val == i:

                k  = key
        print(f'Follow({k}):', follows[i])
    print()
    M = parse_table(result,firsts,follows,terminals, augmentation)
    print()
    print("Parsing string: ")
    print()
    input_string = input("Input string:")
    parse(input_string,start,M)

