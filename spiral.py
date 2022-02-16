import matplotlib.pyplot as plt
import numpy as np
fig, ax = plt.subplots()

def rotate(x,y, alpha,r=None):
    rho = np.sqrt((x*x)+(y*y))
    cosphi = x/rho
    sinphi = y/rho
    if not r:
        newx = ((np.cos(alpha)*cosphi)-(np.sin(alpha)*sinphi))*rho
        newy = ((np.sin(alpha)*cosphi)+(np.cos(alpha)*sinphi))*rho
    else:
        newx = ((np.cos(alpha)*cosphi)-(np.sin(alpha)*sinphi))*(r+rho)
        newy = ((np.sin(alpha)*cosphi)+(np.cos(alpha)*sinphi))*(r+rho)
    return newx, newy

x=0.1
y=0
a=0.4
b=0
rota=0.1
for i in range(1000):
    newx,newy=rotate(x,y,rota,r=rota/10)
    ax.plot([x,newx],[y,newy],color="red")
    x=newx
    y=newy
    newa,newb=rotate(a,b,rota,r=rota/10)
    ax.plot([a,newa],[b,newb],color="blue")
    a=newa
    b=newb

plt.xlim(-10,10)
plt.ylim(-10,10)
plt.show()