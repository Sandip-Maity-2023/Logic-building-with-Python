def is_odd_even():
    print('Even nums till input')

    for i in range(0,101):
        if i%2==0:
            print(i,end=' ')

    print('\nOdd nums till input')
    
    for i in range(0,101):
        if i%2 !=0:
            print(i,end=' ')
is_odd_even()