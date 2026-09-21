import sys

word = sys.argv
if len(word) == 2:
    word = word[1]
    count = word.count('z')
    if count > 0:
        print("z" * count)
    else:
        print("none")
else:
    print("none")
