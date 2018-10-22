year = 2018
month = 10
day = 22
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
pressres = 50 		# resolution in p axis in hPa

Rdry = 287
Cp = 1004


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
print(page.status_code)

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

	
	
	plt.figure()
	plt.axis([mintemp,maxtemp,minthta,np.max(thta)])
	plt.plot(t,thta,label='TEMP')
	plt.plot(td,thta,label='DWPT')
	plt.scatter(t,thta,label='TEMP')
	plt.scatter(td,thta,label='DWPT')
	
	paxis = np.linspace(maxpress,minpress,int((maxpress-minpress)/pressres)+1)
	for pvar in paxis :
		tmpx = np.linspace(mintemp,maxtemp,10)
		tmpy = (tmpx+273)*(1000.0/pvar)**(float(Rdry)/float(Cp))
		plt.plot(tmpx,tmpy,'g')
		plt.show(block=False)
	

	plt.xlabel('Temperature in C')
	plt.ylabel('Potentail temperature in K')
	plt.grid(True)
	plt.title('Tephigram')
	plt.legend()
	plt.show()
