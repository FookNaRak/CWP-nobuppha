print("Enter a number less than 25")
numin = int(input())
if numin <= 25:
    for i in range(numin, 26):
        print(f'Inside the loop, my variable is {i}')
else:
    print("Error")
