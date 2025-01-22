a,b=1,2.0
sum=a+b
print(sum)

"""a,b=1,"2"
sum=a+b
print(sum) """ #error


a,b=1,"2"
c=int (b)
sum=a+c
print(sum)

a=int(input("Enter a number:"))
b=int(input("Enter a number:"))
print(a+b)