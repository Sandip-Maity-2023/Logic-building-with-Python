import numpy as np
x=np.linspace(0,4*np.pi,100)
y=np.sin(x)
z=np.cos(x)
from matplotlib import pyplot as plt
plt.plot(x,y,'r*',x,z,'gd')
plt.title('graph')
plt.xlabel('x axis')
plt.ylabel('y axis')
plt.legend(['sin','cos'])
a=[23,56,12,7]
plt.pie(a)
plt.show()