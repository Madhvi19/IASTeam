
import threading
from kafka import KafkaProducer
from time import sleep
from json import dumps



def register():
    topic='toMonitorRegister'
    producer = KafkaProducer(bootstrap_servers=['localhost:9092'],
                         value_serializer=lambda x: 
                         dumps(x).encode('utf-8'))

    
    ## Get the name & config from the config file of each comp
    name=""
    group=""
    data = {'name' :name,'group':group}
    producer.send(topic, value=data)
    sleep(1)





def heartBeat():
    topic='toMonitorHeartBeat'
    producer = KafkaProducer(bootstrap_servers=['localhost:9092'],
                         value_serializer=lambda x: 
                         dumps(x).encode('utf-8'))

    data = {'status' : 'Alive'}
    while(True):
        producer.send(topic, value=data)
        # print("hello")
        sleep(5)


def monitor():
    tq=threading.Thread(target=heartBeat)
    tq.start()
    tq.join()




