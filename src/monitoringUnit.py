





def sendToSLM():
    producer = KafkaProducer(bootstrap_servers=['localhost:9092'],
                         value_serializer=lambda x: 
                         dumps(x).encode('utf-8'))

    #send the name of failed service
    #get ack 
    #if not ACKED within some time 
    # unable to start 





def registerServices():

consumer = KafkaConsumer('numtest',
     bootstrap_servers=['localhost:9092'],
     auto_offset_reset='earliest',
     enable_auto_commit=True,
     group_id='my-group',
     value_deserializer=lambda x: loads(x.decode('utf-8')))





     ##INsert into collections db
     #insertone 




#in a thread

def getStatus():

    #reads the collection from the db. onr by one.
    # exitting -(tims- cur tim ) >10 -> fail   
    if(cur_time-stored_time)> 10:
        # remove the entry from db
        sendToSLM()

    #otherwise continue
    while(True):
        monitor the queue contents 
        remove one by one and match the current time 





#Acts as pub and sends data to the SLM's topic in case of node failure