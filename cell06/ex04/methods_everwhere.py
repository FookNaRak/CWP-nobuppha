import sys

def shrink(s):
    print(s[:8])

def enlarge(s):
    print(s + 'Z' * (8 - len(s)))

params = sys.argv[1:]

if len(params) < 1:
    print("none")
else:
    for arg in params:
        if len(arg) > 8:
            shrink(arg)
        elif len(arg) < 8:
            enlarge(arg)
        else:
            print(arg)