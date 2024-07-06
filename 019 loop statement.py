number_of_passengers=5
number_of_baggage=2
security_check=True
for passenger_count in range(1,number_of_passengers+1):
    for baggage_count in range(1,number_of_baggage+1):
        if(security_check==True):
            print("Security check for passenger:",passenger_count,"--baggage:",baggage_count,"baggage cleared")
        else:
            print("Security check for passenger:",passenger_count,"--baggage:",baggage_count,"baggage not cleared")