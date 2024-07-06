import turtle
wn=turtle.Screen()
wn.setup(540,508)
alex=turtle.Turtle()
alex.shape("turtle")
alex.color("blue")
destination="south"
if destination=="north":
    alex.left(90)
    alex.forward(100)
elif destination=="south":
    alex.right(90)
    alex.forward(100)
elif destination=="west":
    alex.right(180)
    alex.forward(100)
elif destination=="east":
    alex.forward(100)
else:
    alex.write("Unknown destination", font =("Arial",16,"normal"))
wn.mainloop()