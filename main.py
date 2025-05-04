import flash
import argparse

parser = argparse.ArgumentParser(
    description = "A not so fast simple interpreter."
)
parser.add_arguments(
    "file",
    nargs = "?",
    help = "Input file."
)
args = parser.parse_args()

flash.init()

if args.file:
    for line in args.file:
        flash.execute(flash.tokenize(line))
else:
    while True:
        cmd = input(">>> ")
        flash.execute(flash.tokenize(cmd))