#now we will write a custom application.
import baseAPI
import time
baseAPI.appInit()
while True:
    time.sleep(4)
    print('running the application')
baseAPI.appExit()
