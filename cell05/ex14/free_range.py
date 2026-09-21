import sys

word = sys.argv
if len(word) == 3:
    start = int(word[1])
    end = int(word[2])
    ans = []
    if start < end:
        for i in range(start, end+1):
            ans.append(i)
    else:
        for i in range(start, end-1, -1):
            ans.append(i)
    print(ans)
else:
    print("none")
