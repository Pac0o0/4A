#Imports from the matplotlib library
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
import matplotlib as mpl
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
#--------------------------------------
import math
import numpy as np
import random

fig = plt.figure()#opens a figure environment
ax = fig.gca(projection='3d') #to perform a 3D plot
X = np.arange(-7, 7, 0.4) #x range
Y = np.arange(-7, 7, 0.4) #y range
X, Y = np.meshgrid(X, Y) #creates a rectangular grid on which to plot the function values (Z)
Z= X**4 - X**3 - 20*X**2 + X + 1 + Y**4 - Y**3 - 20*Y**2 + Y + 1 #defines the function values
surf = ax.plot_surface(X, Y, Z, rstride=1, cstride=1, linewidth=0, antialiased=False, cmap=cm.viridis) #plot definition and options
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')


def g(x,y):
	val = x**4 - x**3 - 20*x**2 + x + 1 + y**4 - y**3 - 20*y**2 + y + 1
	return val


def garray(x,y):
	array = np.zeros(len(x))
	for i in range(len(x)):
		array[i] = f(x[i],y[i])
	return array

def run(k1, k2, t, x0, y0):
	xvec = []
	yvec = []
	x = x0
	y = y0

	#xarr.append(x0)
	for step in t:
		T = 1./step
		
		
		#Palier
		somme = 0
		for m in range(5):
			Dx = k1*math.exp(-1/(1000*T)) * np.random.randn()
			Dy = k1*math.exp(-1/(1000*T)) * np.random.randn()
			newx = x+Dx
			newy = y+Dy
			somme += g(newx,newy)-g(x,y)
		dE = 1./5 * somme
		#print ('dE : ' + str(dE))
		proba  = k2*math.exp(-dE/(1000*T))
		#print('P = ' + str(proba))
		
		#Vraie iteration
		
		Dx = k1*math.exp(-1/(1000*T)) * np.random.randn() # Dx~N(0,k1*e^(-1/1000T))
		Dy = k1*math.exp(-1/(1000*T)) * np.random.randn()
		newx = x+Dx
		newy = y+Dy
			
		if(g(newx, newy) < g(x, y)):
			x = newx
			y = newy
			#print("Accepte \n")		
		else:
			roll = random.random()
			
			#Ligne suivante a commenter si on utilise la methode delta E
			#proba = k2*math.exp(-1/(1000*T))
			
			if roll<=proba:
				x = newx
				y = newy
				#print("Accepte \n")
		xvec.append(x)
		yvec.append(y)
	coords = [xvec, yvec]
	return coords
	
	
if __name__ == '__main__':

	#print(g(0,0))
	
	time = np.arange(1,2000,1)
	
	colors = ['c','r','m','b', 'g', 'y',  'k', 'w']
	
	m = [0,0,0,0,0]
	margin = 0.1
	x0=0
	y0=0
	z0=g(x0,y0)

	
	for i in range(1):
		
		result1 = run(0.1,100,time, x0, y0)
		xres = result1[0]
		yres = result1[1]
		xfinal = xres[len(xres)-1]
		yfinal = yres[len(yres)-1]
		zfinal = g(xfinal,yfinal)
		
		#Comptage des equilibres atteints
		
		if(xfinal < 3.548 + margin and xfinal > 3.548 - margin and yfinal < 3.548 + margin and yfinal > 3.548 - margin): #Le pt final est proche du point m0
			m[0]+=1
		elif(xfinal < -2.823 + margin and xfinal > -2.823 - margin and yfinal <  3.548 + margin and yfinal >  3.548 - margin):
			m[1]+=1
		elif(xfinal < -2.823 + margin and xfinal > -2.823 - margin and yfinal < -2.823 + margin and yfinal > -2.823 - margin):
			m[2]+=1
		elif(xfinal < 3.548 + margin and xfinal > 3.548 - margin and yfinal < -2.823 + margin and yfinal > -2.823 - margin):
			m[3]+=1
		
		
		else: #Equilibre non atteint
			m[4]+=1
			
		
		
		
			
		
		#print('(x,y) final : (' + str(xfinal) + ', ' + str(yfinal) + ')')
		#print('g(x,y) = ' + str(g(xfinal, yfinal))+'\n')
		
		#Affichage des trajectoires
		
		zres = []
		for j in range(len(xres)):
			zres.append(g(xres[j],yres[j]))
		ax.plot(xres,yres,zres,color='r')
		
		'''
		#Affichage des points finaux
	for i in range(len(m)):
		if(i==0):
			ax.plot([3.548], [3.548], [g(3.548,3.548)], markerfacecolor='g', markeredgecolor='g', marker='o', markersize=0.5*m[i], alpha=0.6)
		elif i==1:
			ax.plot([-2.823], [3.548], [g(-2.823,3.548)], markerfacecolor='g', markeredgecolor='g', marker='o', markersize=0.5*m[i], alpha=0.6)
		elif i==2:
			ax.plot([-2.823], [-2.823], [g(-2.823,-2.823)], markerfacecolor='g', markeredgecolor='g', marker='o', markersize=0.5*m[i], alpha=0.6)
		elif i==3:
			ax.plot([3.548], [-2.823], [g(3.548,-2.823)], markerfacecolor='g', markeredgecolor='g', marker='o', markersize=0.5*m[i], alpha=0.6)
		
	'''
	
	#Affichage des points d'equilibres atteint	
	print(m)
	
	#Affichage des points de depart
	ax.plot([x0], [y0], [g(x0,y0)], markerfacecolor='m', markeredgecolor='w', marker='o', markersize=5, alpha=0.6)
	plt.show()
