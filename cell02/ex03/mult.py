fnum = int(input())
snum = int(input())
result = fnum * snum
print(f"{fnum} x {snum} = {result}")
if result > 0:
    print("The result is positive.")
elif result == 0:
    print("The result is positive and negative.")
else:
    print("The result is negative.")
