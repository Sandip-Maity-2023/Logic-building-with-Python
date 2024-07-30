p=int(input("Enter the value of principle amount:"))
r=int(input("Enter the value of rate of interest:"))
t=int(input("Enter the value of time period:"))
interest=(p*r*t)/100
print("Simple interest:",interest)
print("Total Amount(principle + interest):",p+interest)