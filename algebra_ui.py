import algebra_classes as alg_cl

def close():
    '''Closes this application.'''
    global GOODBYE
    print(GOODBYE)
    raise SystemExit

def solve(exp_str: str):
    '''The main solver function.'''
    exp, vars_dict = identify(exp_str)
    pass

def identify(exp_str: str):
    '''The main identification function.'''
    global OPERATIONS
    #find longest operation length
    length = len(OPERATIONS.copy().popitem()[0])
    for op in OPERATIONS:
        if len(op) > length:
            length = len(op)
    ops = []
    #order operations into list from largest to smallest
    while length > 0:
        for key in OPERATIONS:
            if len(key) == length:
                ops.append(key)
        length -= 1
    #break expression into parts
    parts = break_apart(ops, [exp_str.replace(' ','')])
    #report expression parts
    parts_str = ''
    for part in parts:
        parts_str += part + ' , '
    parts_str = parts_str[0:-3]
    print('|identified parts: '+parts_str+' ...')
    #classify constants and variables
    parts = alg_cl.Constant.classify(parts)
    parts = alg_cl.Variable.classify(parts)
    #collate dictionary of identified variables
    vars_dict = dict()
    for part in parts:
        if isinstance(part, alg_cl.Variable):
            vars_dict.setdefault(part.name)
    #report identified variables
    vars_str = ''
    for key in vars_dict:
        vars_str += key + ' , '
    vars_str = vars_str[0:-3]
    print('|identified variables: '+vars_str+' ...')
    #classify operations
    parts = alg_cl.Product.classify(*parts)
    parts = alg_cl.Sum.classify(*parts)
    #classify equation
    for part in parts:
        if isinstance(part, str):
            exp = OPERATIONS[part][1].classify(*parts)
            break
    #report identification completion
    print('|identification successful: '+str(exp)+' ...')
    return (exp, vars_dict)

def break_apart(seps: list, exp: list) -> list:
    '''Breaks given exp into parts using ops separators.'''
    for sep in seps:
        i = 0
        while i < len(exp):
            part = exp.pop(i)
            if part.count(sep) > 0 and len(part) > len(sep):
                parts = part.partition(sep)
                for item in parts:
                    exp.insert(i, item)
                    i += 1
                exp = break_apart(seps, exp)
            else:
                exp.insert(i, part)
                i += 1
    return exp
    
def commands():
    '''Prints supported commands.'''
    global COMMANDS
    print('\nCommands:')
    for com in COMMANDS:
        print(com + ' : ' + COMMANDS[com][0])
    return

def operations():
    '''Prints list of supported operations.'''
    global OPERTIONS
    print("\nSupported operations:")
    for op in OPERATIONS:
        print(op + ' : ' + OPERATIONS[op][0])
    return

def validate_com(inp : str):
    '''Validates existence of command and correct number of arguments.'''
    global COMMANDS, NOT_FOUND, MANY_ARGS, FEW_ARGS
    #refine input
    com = inp.partition(' ')[0]
    args = inp.partition(' ')[2]
    #check command existence
    for command in COMMANDS:
        if com == command:
            break
    else:
        print(NOT_FOUND)
        return
    #check correct number of arguments
    if bool(args) > COMMANDS[com][1]:
        print(MANY_ARGS)
        return
    elif bool(args) < COMMANDS[com][1]:
        print(FEW_ARGS)
        return
    #execute command
    print('|executing ' + com + '(' + args + ')...')
    if COMMANDS[com][1] != 0:
        COMMANDS[com][2](args)
    else:
        COMMANDS[com][2]()
    return

WELCOME = "Welcome to the Mader Algrebraic Expression Solver."
COMMANDS = {'close' : ('closes this application', 0, close),
            'coms' : ('displays this command list', 0, commands),
            'ops' : ('displays a list of supported operations', 0, operations),
            'solve' : ('solves the following algebraic expression', 1, solve)}
OPERATIONS = {'+' : ('addition', alg_cl.Sum),
              '*' : ('multiplication', alg_cl.Product),
              '=' : ('equal to', alg_cl.Equal),
              '>' : ('greater than', alg_cl.Greater),
              '<' : ('lesser than', alg_cl.Lesser),
              '>=' : ('greater than or equal to', alg_cl.GreaterEqual),
              '<=' : ('lesser than or equal to', alg_cl.LesserEqual),
              '!=' : ('not equal to', alg_cl.NotEqual)}
BRACKETS = {'(' : ')',
            '[' : ']',
            '{' : '}'}
GOODBYE = "\nThank you for using the Mader Algebraic Expression Solver."
COM_PROMPT = "\ncommand> "
NOT_FOUND = "!command not found. check the supported commands"
MANY_ARGS = "!too many arguments inputted"
FEW_ARGS = "!too few arguments inputted"


print(WELCOME)
commands()
while True:
    com = input(COM_PROMPT)
    validate_com(com)
