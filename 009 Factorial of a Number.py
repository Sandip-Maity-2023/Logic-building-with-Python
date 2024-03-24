def factorial(n):
    if n == 0:
        return 1
    else:
        return n * factorial(n - 1)
num = float(input("Enter a number:"))
print("Factorial:", factorial(num))
