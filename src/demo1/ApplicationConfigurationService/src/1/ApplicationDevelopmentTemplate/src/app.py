#now we will write a custom application.
import baseAPI
import time
from Bulb import Bulb
baseAPI.appInit()
firstBulb=Bulb('primary_label')
secondBulb=Bulb('secondy_label')

while True:
    time.sleep(4)
    a=firstBulb.getcolor()
    print('running the application')
    if a>10:
        d={'intensity':10}
        print('cahnging the color intensity')
        secondBulb.changeIntensity(d)
baseAPI.appExit()
