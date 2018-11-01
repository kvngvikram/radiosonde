# This code takes the Radiosonde data from the website http://weather.uwyo.edu/upperair/sounding.html
# For any issue contact kvng vikram 

year = 2018
month = 9
day = 27
time = 00
code = 43371

ask = False	# set true if you want program to ask for a date to look at


mintemp = -100		# C
maxtemp = 40		# C
minthta = 280		# K
maxthta = 1000

# pressure axis range
minpress = 100 		# hPa
maxpress = 1050		# hPa
pressres = 50		# resolution in p axis in hPa

# For constant mixing ration lines in g/kg
waxis = [0.01,0.05,0.1,0.2,0.35,0.5,0.75,1,1.5,2,3,4,5.5,6.5,8,10,12,16,20,24,28,32,40,48,56,64,72]

# constants 
Rdry = 287.05		# J/(kg K)
Rvap = 461.52		# J/(kg K)
L = 2.27*10**6		# J/kg	
Ttp = 0.01		# C
Etp = 6.11657		# hPa
Cp = 1004.0
CK = 273.0		# centrigrade to kelvin conversion offset
Epsilon = Rdry/Rvap 


if ask :
	print('\n\n\n\t\tGive the details of the date of the data\n\n')
	date = input('\t\tdate\t:\t')
	month = input('\t\tmonth\t:\t')
	year = input('\t\tyear\t:\t')
	print('\n\n\n')

from bs4 import BeautifulSoup as mbs
import requests
import numpy as np
import matplotlib.pyplot as plt 

year = str(year)
month = str(month) if (int(month)>=10) else ('0'+str(month))
day = str(day) if (int(day) >= 10) else ('0'+str(day))
code = str(code)


webaddress = 'http://weather.uwyo.edu/cgi-bin/sounding?region=seasia&TYPE=TEXT%3ALIST&YEAR='+year+'&MONTH='+month+'&FROM='+day+'00&TO='+day+'00&STNM='+code

page = requests.get(webaddress)
#print('connection successful' if page.status_code == 200 else 'connection failed')

soup = mbs(page.text,'html.parser')
#print(soup)

dat = soup.find("pre")
#print(dat)

if dat is None :
	print('\n\n\n\tSomething went wrong dude.')
	print('\n\tCheck if you have given the right dates.')
	print('\n\tIf nothing works then call KVNG Vikram, and both of you search in google together.\n\n\n\n')

else : 
	# not mydat is a string
	mydat = str(dat)
	#print(mydat)

	# removing the headders and other characters so that only numbers are left 
	mydat = mydat[318:len(mydat)-7]
	#print(mydat)

	# removing the last line of data as it can be incomplete
	mydata = mydat[:len(mydat)-78]
	#print(mydata)

	lines = mydata.splitlines()

	p = np.array([])
	h = np.array([])
	t = np.array([])
	td = np.array([])
	rh = np.array([])
	w = np.array([])
	d = np.array([])
	v = np.array([])
	thta = np.array([])
	thte = np.array([])
	thtv = np.array([])

	for i in range(len(lines)):
		dummy = lines[i].split()
		p    = np.pad(p,(0,1),'constant',constant_values = float(dummy[0]))
		h    = np.pad(h,(0,1),'constant',constant_values = float(dummy[1]))
		t    = np.pad(t,(0,1),'constant',constant_values = float(dummy[2]))
		td   = np.pad(td,(0,1),'constant',constant_values = float(dummy[3]))
		rh   = np.pad(rh,(0,1),'constant',constant_values = float(dummy[4]))
		w    = np.pad(w,(0,1),'constant',constant_values = float(dummy[5]))
		d    = np.pad(d,(0,1),'constant',constant_values = float(dummy[6]))
		v    = np.pad(v,(0,1),'constant',constant_values = float(dummy[7]))
		thta = np.pad(thta,(0,1),'constant',constant_values = float(dummy[8]))
#		thte = np.pad(thte,(0,1),'constant',constant_values = float(dummy[9]))
#		thtv = np.pad(thtv,(0,1),'constant',constant_values = float(dummy[10]))



	def PT_to_ThetaT(P,T):		# Units : hPa,C to K,C
		return (T+CK)*(1000.0/P)**(Rdry/Cp) , T 

	def ThetaT_to_PT(Theta,T):	# Units : K,C to hPa,C
		return 1000.0*((T+CK)/Theta)**(Cp/Rdry) , T	# from Poisson's equation
		
	def WT_to_PT(W,T):		# Units : g/kg,C to hPa,C
		return ((Epsilon+(W/1000.0))/(W/1000.0))*Etp*np.exp((1/(Ttp+CK)-1/(T+CK))*L/Rvap) , T 

	plt.figure()
	plt.axis([mintemp,maxtemp,minthta,np.max(thta)])
	
	# plotting each isobar in a loop
	paxis = np.linspace(maxpress,minpress,int((maxpress-minpress)/pressres)+1)
	for pvar in paxis :
		tmpx = np.linspace(mintemp,maxtemp,2)
		tmpy,tmpx = PT_to_ThetaT(pvar,tmpx)
		plt.plot(tmpx,tmpy,'g',linewidth=0.5)
	
	for wvar in waxis:
		tmpx = np.linspace(mintemp,maxtemp,50)
		tmpp , tmpx = WT_to_PT(wvar,tmpx)
		tmpy , tmpx = PT_to_ThetaT(tmpp,tmpx)
		plt.plot(tmpx,tmpy,'r',linewidth=0.5)
	
	plt.xlabel('Temperature in C')
	plt.ylabel('Potentail temperature in K')
	plt.grid(True)
	plt.title('Tephigram')
#	plt.legend()
	
	TdTheta,td =  PT_to_ThetaT(p,td)
	TTheta , t =  PT_to_ThetaT(p, t)
	
	plt.plot(t,TTheta,label='TEMP',linewidth=2)
	plt.plot(td,TdTheta,label='DWPT',linewidth=2)
	plt.scatter(t,TTheta,label='TEMP',s=10)
	plt.scatter(td,TdTheta,label='DWPT',s=10)
	
	plt.show()
