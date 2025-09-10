"""def sim_interest():

    p=int(input('Enter principle: '))
    r=int(input('Enter rate of interest: '))
    t=int(input('Enter time: '))
    i=p*r*t/100
    print('Simple Interest :',i)
sim_interest() """

def simple_interest(p,r,t):
    return p*r*t/100
def get_float(prompt):
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print('Invalid Input,Please enter a number: ')
def main():
    p=get_float("Enter principle: ")
    r=get_float("Enter rate of interest: ")
    t=get_float("Enter time: ")
    # 'in' is a reserved keyword in Python inline """ does not allow
    ini=simple_interest(p,r,t)
    print(f"simple interest:{ini}")

    if __name__=="__main__":
        main()
