# This code is to get the tephigrams from Indian Meteorological Department website
# For any isseus please contact KVNG Vikram


# Adress of sonder image for required location can by selected from the map http://satellite.imd.gov.in/map_skm2.html 
# use that address below (Use http:// )
address = 'http://satellite.imd.gov.in/img/Thiruvanantapurum.gif'


import requests
from PIL import Image


response = requests.get(address,stream=True).raw

im = Image.open(response)
im.show()

