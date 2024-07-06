'''x=(1,5,7)
product=1
i=0
if(x[2]==7):
    print (-1)
else:
while(x==7):
    x[7]=x[i]
    i=i+1
product=product*x[i+1]
print(product)'''
def product_excluding_7(values):
    # Check if 7 is in the tuple
    if 7 in values:
        # Find the index of 7
        index_7 = values.index(7)
        # Get the values to the right of 7
        values = values[index_7 + 1:]

    # If no values remain after 7, return -1
    if len(values) == 0:
        return -1

    # Calculate the product of the remaining values
    product = 1
    for value in values:
        product *= value

    return product

# Test cases
print(product_excluding_7((1, 5, 3)))  # Output: 15
