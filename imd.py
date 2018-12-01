# This code is to get the tephigrams from Indian Meteorological Department website
# For any isseus please contact KVNG Vikram



address = 'http://satellite.imd.gov.in/img/Thiruvanantapurum.gif'


import requests
from PIL import Image

f = open('temp_image.gif','wb')
f.write(requests.get(address).content)
f.close()

im = Image.open('temp_image.gif')
im.show()

