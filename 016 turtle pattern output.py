import turtle      #turtle is a library
wn=turtle.Screen()
wn.setup(400,400)
circle_rad=50
rectangle_width=150
rectangle_height=80
alex=turtle.Turtle()
alex.shape("turtle")
alex.color('red')
alex.circle(circle_rad)
alex.backward(rectangle_width/2)
alex.forward(rectangle_width)
alex.right(90)
alex.forward(rectangle_height)
alex.right(90)
alex.forward(rectangle_width)
alex.right(90)
alex.forward(rectangle_height)