"""
flash: Not so fast simple interpreter.

Keywords:
- add, sub, mul, div, mod, pow, sqrt, cbrt, abs
- print, blank, load, copy, swap
- ieq, ine, igt, ilt, ige, ile
- return, halt
- sleep
- round, floor, ceil
- and, or, xor, not
- nop

Functions:
- init
- tokenize
- execute
"""

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
    global csv
    global io
    csv = __import__("csv")
    io = __import__("io")
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
    if kword == "nop":
        return
    elif kword == "halt":
        exit(130)
    if len(token) == 1:
        raise e.ArgumentError("No argument provided.")
    args = token[1:]
    if kword in ["add", "sub", "mul", "div", "mod", "pow"]:
        if len(args) != 3:
            raise e.ArgumentError(f"Excepted 3 arguments ({len(args)} given).")
        reg1 = args[0]
        reg2 = args[1]
        dest = args[2]
        if reg1 not in regs:
            raise e.RegisterError(f"Register '{reg1}' is not a valid register.")
        if reg2 not in regs:
            raise e.RegisterError(f"Register '{reg2}' is not a valid register.")
        if reg1[-1] != "n":
            raise e.RegisterError(f"Register '{reg1}' is not a number register.")
        if reg2[-1] != "n":
            raise e.RegisterError(f"Register '{reg2}' is not a number register.")
        if regs[reg1] == None:
            raise e.RegisterError(f"Register '{reg1}' is not assigned to any value.")
        if regs[reg2] == None:
            raise e.RegisterError(f"Register '{reg2}' is not assigned to any value.")
        if regs[dest] != None:
            raise e.RegisterError(f"Register '{dest}' is assigned to value '{regs[dest]}'.")
        if kword == "add":
            regs[dest] = regs[reg1] + regs[reg2]
        elif kword == "sub":
            regs[dest] = regs[reg1] - regs[reg2]
        elif kword == "mul":
            regs[dest] = regs[reg1] * regs[reg2]
        elif kword == "div":
            regs[dest] = regs[reg1] / regs[reg2]
        elif kword == "mod":
            regs[dest] = regs[reg1] % regs[reg2]
        elif kword == "pow":
            regs[dest] = regs[reg1] ** regs[reg2]
    elif kword in ["print", "blank"]:
        if len(args) != 1:
            raise e.ArgumentError(f"Expected 1 argument ({len(args)} given).")
        reg = args[0]
        if reg not in regs:
            raise e.RegisterError(f"Register '{reg}' is not a valid register.")
        if kword == "print":
            print(regs[reg])
        elif kword == "blank":
            regs[reg] = None
    elif kword in ["ieq", "ine", "igt", "ilt", "ige", "ile"]:
        if len(args) != 3:
            raise e.ArgumentError(f"Expected 3 arguments ({len(args)} given).")
        reg1 = args[0]
        reg2 = args[1]
        reg3 = args[2]
        if reg1[-1] != reg2[-1]:
            raise e.RegisterError(f"Registers '{reg1}' and '{reg2}' are not the same type.")
        if reg3[-1] != "b":
            raise e.RegisterError(f"Register '{reg3}' is not a bool register.")
        if regs[reg1] == None:
            raise e.RegisterError(f"Register '{reg1}' is not assigned to any value.")
        if regs[reg2] == None:
            raise e.RegisterError(f"Register '{reg2}' is not assigned to any value.")
        if kword == "ieq":
            regs[reg3] = regs[reg1] == regs[reg2]
        elif kword == "ine":
            regs[reg3] = regs[reg1] != regs[reg2]
        elif kword == "igt":
            regs[reg3] = regs[reg1] > regs[reg2]
        elif kword == "ilt":
            regs[reg3] = regs[reg1] < regs[reg2]
        elif kword == "ige":
            regs[reg3] = regs[reg1] >= regs[reg2]
        elif kword == "ile":
            regs[reg3] = regs[reg1] <= regs[reg2]
    elif kword in ["copy", "swap"]:
        if len(args) != 2:
            raise e.ArgumentError(f"Expected 2 arguments ({len(args)} given).")
        reg1 = args[0]
        reg2 = args[1]
        if reg1[-1] != reg2[-1]:
            raise e.RegisterError(f"Registers '{reg1}' and '{reg2}' are not the same type.")
        if regs[reg1] == None:
            raise e.RegisterError(f"Register '{reg1}' is not assigned to any value.")
        if kword == "copy":
            if regs[reg2] != None:
                raise e.RegisterError(f"Register '{reg2}' is assigned to value '{regs[reg2]}'.")
            regs[reg2] = regs[reg1]
        elif kword == "swap":
            if regs[reg2] == None:
                raise e.RegisterError(f"Register '{reg2}' is not assigned to any value.")
            temp = regs[reg2]
            regs[reg2] = regs[reg1]
            regs[reg1] = temp