print(2**(3**2))
print((2**3)*2)
print(2**3**2)
#print(2**(3**2)): This expression raises 3 to the power of 2 first (resulting in 9), and then 2 to the power of 9, which is 512.
#print((2**3)*2): This expression calculates 2 to the power of 3 (which is 8), then multiplies it by 2, resulting in 16.
#print(2**3**2): This expression is a bit different due to the nature of exponentiation. In Python (and in most programming languages), exponentiation (**) is right-associative, meaning it evaluates from right to left. So, it's equivalent to 2**(3**2). This expression calculates 3 to the power of 2 first (resulting in 9), and then 2 to the power of 9, which, as we know from the first expression, is 512.