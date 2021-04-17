#now we will write a custom application.
import baseAPI
import room
import time
import Bulb
baseAPI.appInit()
myroom=room('joke')
numBulb=myroom.getSensorCount('Bulb')
for i in range(numBulb):
    tempLabel=myroom.getSensorLabel('Bulb',i)
    b=Bulb(tempLabel)
    print(b.getcolor())
baseAPI.appExit()
