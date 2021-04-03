
#acts as a consumer of monitoringUnit
#get the corresponding  code from the platform repo
# Go to a freely avaialble server by ssh
# run nodeUnit.py on it

#run the failed service on the new node

from kafka import KafkaConsumer
from json import loads
consumer = KafkaConsumer(
    'numtest',
     bootstrap_servers=['localhost:9092'],
     auto_offset_reset='earliest',
     enable_auto_commit=True,
     group_id='my-group',
     value_deserializer=lambda x: loads(x.decode('utf-8')))



