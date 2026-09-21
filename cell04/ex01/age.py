age = int(input("Please tell me your age: "))
print(f"You are currently {age} years old.")

for i in range(1,4):
    year = 10*i
    age += 10
    print(f"In {year} years, you'll be {age} years old.")
