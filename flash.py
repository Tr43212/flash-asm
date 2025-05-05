import csv
import io

class e:
    class KeywordError(Exception):
        def __init__(self, msg):
            super().__init__(msg)
    class ArgumentError(Exception):
        def __init__(self, msg):
            super().__init__(msg)
    class RegisterError(Exception):
        def __init__(self, msg):
            super().__init__(msg)

def init():
    global regs
    regs = {}
    for i in range(1, 11):
        for char in "nsb":
            regs[f"r{i}{char}"] = None

def tokenize(cmd):
    parts = cmd.split(maxsplit = 1)
    if len(parts) == 0 or len(parts) == 1:
        return parts
    kword = [parts[0]]
    args = next(csv.reader(io.StringIO(parts[1]), skipinitialspace = True))
    return kword + args

def execute(token):
    if len(token) == 0:
        raise e.KeywordError("No keyword provided.")
    kword = token[0]
    if len(token) == 1:
        raise e.ArgumentError("No argument provided.")
    args = token[1:]
    if kword in ["add", "sub", "mul", "div", "mod"]:
        if len(args) != 3:
            raise e.ArgumentError(f"Excepted 3 arguments ({len(args)} given)")
        reg1 = args[0]
        reg2 = args[1]
        dest = args[2]
        if regs[reg1] == None:
            raise e.RegisterError(f"Register '{reg1}' is not assigned to any value.")
        if regs[reg2] == None:
            raise e.RegisterError(f"Register '{reg2}' is not assigned to any value.")
        if regs[dest] != None:
            raise e.RegisterError(f"Register '{dest}' is stored value '{regs[dest]}'.")
    # more soon im lazy