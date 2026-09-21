import sys

word = sys.argv
if len(word) >= 2:
    for w in word[1:]:
        if not w.endswith("ism"):
            print(w + "ism")
else:
    print("none")
