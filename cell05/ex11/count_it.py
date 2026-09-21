import sys

params = sys.argv[1:]

if len(params) == 0:
    print("none")
else:
    print(f"parameters: {len(params)}")
    for p in params:
        print(f"{p}: {len(p)}")
