import numpy as np
import matplotlib.pyplot as plt


data = np.genfromtxt('data18.csv',delimiter = '\t',dtype=float)

t , elv , azm  = data[:,0] , data[:,1] , data[:,2] 

w = float(9.0/60.0)
z = t*w 

d = z/np.tan(np.deg2rad(elv)) 

x = d*np.sin(np.deg2rad(azm))

y = d*np.cos(np.deg2rad(azm))  

dx = np.diff(x)
dy = np.diff(y)
dt = np.diff(t)

V = (((dx**2 + dy**2)**.5)/dt)*(1000/60)
u = (dx/dt)*(1000/60)
v = (dy/dt)*(1000/60)
phi = np.rad2deg(np.arctan(dy/dx))
phi = np.logical_and(v>0,u>0).astype(float)*abs(phi) + np.logical_and(v>0,u<0).astype(float)*(abs(phi)+90) + np.logical_and(v<0,u<0).astype(float)*(abs(phi)+180) + np.logical_and(v<0,u>0).astype(float)*(abs(phi)+270)




plt.figure()

plt.subplot(2,2,1)	# for trajectory 
#plt.axis([-1,0.5,-.5,.5])
plt.grid(True)
plt.title('Balloon trajectory')

plt.subplot(2,2,2)	# for the velocity vectors 
#plt.axis([-5,3,-4,4])
plt.grid(True)
plt.title('Velocity vector')

plt.subplot(2,2,3)
plt.title('wind with height')
plt.grid(True)
#plt.axis([0,2,0,5])

plt.subplot(2,2,4)
plt.title('wind direction with height')
plt.grid(True)
#plt.axis([0,2,-180,180])

# size of V is smaller by size of x or y or z by 1
for i in range(np.size(V)-1):

	plt.subplot(2,2,1)
	plt.plot([x[i],x[i+1]],[y[i],y[i+1]],'b')
	
	plt.subplot(2,2,2)
	plt.plot([0,u[i]],[0,v[i]],'r')

	plt.subplot(2,2,3) 
	plt.plot([z[i],z[i+1]],[V[i],V[i+1]],'b')

	plt.subplot(2,2,4) 
	plt.plot([z[i],z[i+1]],[phi[i],phi[i+1]],'b')
	
	plt.show(block=False)
	plt.pause(0.1) 


plt.subplot(2,2,1)
plt.plot([x[np.size(z)-2],x[np.size(z)-1]],[y[np.size(z)-2],y[np.size(z)-1]],'b')

plt.subplot(2,2,2)
plt.plot([0,u[np.size(V)-1]],[0,v[np.size(V)-1]],'r')
plt.plot(u,v,'b')

print('done')
plt.show()



