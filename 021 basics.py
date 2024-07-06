list_of_airlines=["AI","EM","BA"]
print("List of airlines:",list_of_airlines)

sample_list=["Mark",5,"Jack",9,"Chan",5]
print("Sample List:",sample_list)

sample_list.append("James")
print("After adding element to list:",sample_list)

new_list=["Henry","Tim"]
sample_list+=new_list

print("After combining two lists-1st way:",sample_list)

print(sample_list[6])

list_of_airlines=["AI","EM","BA"]
print("Iterating the list using range()")

for index in range(0,len(list_of_airlines)):
    print(list_of_airlines[index])

for airline in list_of_airlines:
        print(airline)

airline_details=[["AI",8], ["EM",10],["BA",7]]

#To get the details of Emirates (EM) airline
#Prints a list
print(airline_details[1])

#To get the number of flights operated by British Airways (BA)
#[2][1] refers to 2nd list and 1st value, inside airline_details
#Remember counting is 0 based
print(airline_details[2][1])

#To display the details of all airlines
print("Airline details as a list:")
for airline in airline_details:
    print(airline)

#To display the number of flights operated by each airline
print("No. of flights operated by each airline:")
for airline in airline_details:
        print(airline[1])    
