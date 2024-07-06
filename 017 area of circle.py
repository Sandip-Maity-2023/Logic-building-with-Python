import math
def area_of_circle(radius):
    if radius<=0:
        return "radius cannot be negative"
    return math.pi*radius**2
radius=float(input("Enter the radius of the circle:"))
area=area_of_circle(radius)
print(f"The area of the circle with {radius} is :{area}")