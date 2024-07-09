from collections import Counter
def find_max_departures(flights):

    flights_counts=Counter(flights)   #find number of flights to each country
    max_country = max(flights_counts, key=flights_counts.get)    #find the country of maximum number of flights
    return max_country
flights = ["india","china","cuba","brazil","jordan","india","china","india","india"]    #flights data
max_country = find_max_departures(flights)
print("country with maximum number of flights:", max_country)