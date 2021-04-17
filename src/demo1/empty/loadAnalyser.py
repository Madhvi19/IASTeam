import psutil
def getCpuUsage():
    summ=0
    cnt=3
    for i in range(cnt):
        summ+=psutil.cpu_percent(interval=0.1)
    return summ/cnt
def getMemUsage():
    return psutil.virtual_memory().percent 