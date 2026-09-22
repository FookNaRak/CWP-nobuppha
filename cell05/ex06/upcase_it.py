import sys

params = sys.argv[1:]

if len(params) != 1:
    print("none")
else:
    print(params[0].upper())
