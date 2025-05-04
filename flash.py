class e:
    class KeywordError(Exception):
        def __init__(self, msg: str) -> None:
            super().__init__(msg)
    class ArgumentError(Exception):
        def __init__(self, msg: str) -> None:
            super().__init__(msg)
    class RegisterError(Exception):
        def __init__(self, msg: str) -> None:
            super().__init__(msg)

def init() -> None:
    import csv
    import io
    global regs
    regs: dict[str, int | float | str | bool] = {}
    for i in range(1, 11):
        for char in "nsb":
            regs[f"r{i}{char}"] = None

def tokenize(cmd) -> list[str]:
    parts: list = cmd.split(maxsplit = 1)
    if len(parts) == 0 or len(parts) == 1:
        return parts
    kword: list[str] = [parts[0]]
    args: list[str] = next(csv.reader(io.StringIO(parts[1]), skipinitialspace = True))
    return kword + args