def add_to_grammar(str,grammar={}):
    x = str.split("->")
    y = x[1]
    x.pop()
    z = y.split("|")
    x.append(z)
    grammar[x[0]]=x[1]
    return grammar


def format_output(y):
    output = ''
    if isinstance(y,type([])):
        for l in y:
            output += ''.join(l)
            output += '|'
        if output[-1] == '|':
            output = output[:-1]
    else:
        output = y
    # print(output)

    return output
