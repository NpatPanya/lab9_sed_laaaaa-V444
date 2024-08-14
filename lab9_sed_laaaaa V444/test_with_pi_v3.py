# python 3.6import random
import time
import random
import json
import pymongo
# import RPi.GPIO as GPIO
from paho.mqtt import client as mqtt_client


import multiprocessing
print("Number of cpu : ", multiprocessing.cpu_count())

broker = 'm15.cloudmqtt.com'
port = 12987
client_id = f'python-mqtt-{random.randint(0, 1000)}'
username = 'cyejnmdr'
password = 'Is7roaqnQX09'

mongo_client = pymongo.MongoClient('mongodb+srv://npatonpym:B1o2s4s5@cluster0.ztybuzz.mongodb.net/')

# Define GPIO pins for sensors
# TEMP_PIN = 17
# HUMIDITY_PIN = 18
# EC_PIN = 19
# PH_PIN = 20
# N_PIN = 21
# P_PIN = 22
# K_PIN = 23
LIGHT_PIN = 24
PUMP_PIN = 23
# SPRAY_PIN = 25
FERTILIZER_PIN = 25

def publish_to_mongodb(device, message,client):
    try:
        db = mongo_client['test']
        collection = db['device_statuses']
        data = {"device": device, "status": message}
        print("data_to_mongo",data)
        collection.insert_one(data)
        print("data_to_mongo_succesfull")

        client.publish("mongodb_status", "Data inserted into MongoDB successfully")
    except Exception as e:
        print("Error inserting data into MongoDB:", e)
        client.publish("mongodb_status", f"Error: {e}")

  
def connect_mqtt() -> mqtt_client:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client
def publish(client):

    msg_count = 0
    while True:
        time.sleep(3)
        topic="tttt"
        msg = f"{msg_count+1},{msg_count+2},{msg_count+3},{msg_count+4},{msg_count+5},{msg_count+6},{msg_count+7}"
        # msg = f"{humidity_sensor},{temperature},{EC_sensor},{PH_sensor},{N_meter},{P_meter},{K_meter}"
        result = client.publish(topic, msg)
        # result: [0, 1]
        print(msg)
        if msg_count==100:
           msg_count =0
        else:
           msg_count+=1


def subscribe(client: mqtt_client):
    client.subscribe("testsenddevicestatus")
    client.subscribe("testsenddeviceInterval")
    client.subscribe("wbutto")
    client.subscribe("sbutto")
    client.subscribe("fbutto")
    client.subscribe("lbutto")
    client.on_message = on_message #"waterpump,on" "waterpump,off","medpump,on"
    
def on_message(client, userdata, msg):
    
    # print(f"Received device: {device}, Status: {status}")
    if msg.topic == "testsenddevicestatus":
        message = msg.payload.decode("utf-8")  # Parse the JSON payload
        payload = json.loads(message)
        device = payload["device"]  # Extract the value of the "device" key
        status = payload["state"] # Extract the value of the "status" key
        # print(device," : ",status)
        if device == "waterpump":
            pump = status
            print(device,pump)

        elif device == "bugkiller":
            spray = status
            print(device,spray)

        elif device == "fertilizer":
            fertilizer = status
            print (device,fertilizer)

        elif device == "Light":
            light_bulb = status
            print (device,light_bulb)
            
    elif msg.topic == "testsenddeviceInterval":
        message =msg.payload.decode("utf-8") # Parse the JSON payload
        payload = json.loads(message)
        Idevice = payload["type"]  # Extract the value of the "device" key
        Interval = payload["Interval"] # Extract the value of the "status" key
        # print(Idevice," : ",Interval)
        if Idevice == "WaterPump":
            Ipump = int(Interval)
            #print(type(Ipump))
            print(Idevice,Ipump)

        if Idevice == "Spray":
            Ispray = int(Interval)
            #print(type(Ispray))
            print(Idevice,Ispray)

        if Idevice == "Fertilizer":
            Ifertilizer = int(Interval)
            #print(type(Ifertilizer ))
            print(Idevice,Ifertilizer )

        if Idevice == "Light":
            ILight = int(Interval)
            # print(type(ILight ))
            print(Idevice,ILight )


    elif msg.topic == "wbutto":
        message =msg.payload.decode("utf-8") # Parse the JSON payload
        device = "Waterpump"
        topic = "mobileToDB"
        # print(message)
        if message == "On":
            GPIO.output(PUMP_PIN.LOW)
            print("Waterpump",":", message)
        else :
            GPIO.output(PUMP_PIN.HIGH)
            print("Waterpump",":", message)
        
        response_msg = f"{device},{message}"
        try:
            # client.publish(topic, response_msg)
            publish_to_mongodb(device, message,client)
        except Exception as e:
            
            print("Error:", e)
            

    elif msg.topic == "lbutto":
        message =msg.payload.decode("utf-8") 
        device = "Light"
        topic = "mobileToDB"
        # print(message)
        if message == "On":
            GPIO.output(PUMP_PIN.HIGH)
            print("Light",":", message)
        else :
            GPIO.output(PUMP_PIN.LOW)
            print("Light",":", message)
        
        response_msg = f"{device},{message}"
        try:
            
             # client.publish(topic, response_msg)
            publish_to_mongodb(device, message,client)
        except Exception as e:
            
            print("Error:", e)
            

    elif msg.topic == "fbutto":
        message = msg.payload.decode("utf-8") # Parse the JSON payload
        device = "Fertilizer"
        topic = "mobileToDB"
        # print(message)
        if message == "On":
            GPIO.output(FERTILIZER_PIN.LOW)
            print("Fertilizer",":", message)
        else :
            GPIO.output(FERTILIZER_PIN.HIGH)
            print("Fertilizer",":", message)

        response_msg = f"{device},{message}"
        try:
           
             # client.publish(topic, response_msg)
            publish_to_mongodb(device, message,client)
        except Exception as e:
            
            print("Error:", e)
            

    elif msg.topic == "sbutto":
        message =msg.payload.decode("utf-8") # Parse the JSON payload
        device = "Spray"
        topic = "mobileToDB"
        # print(message)
        if message == "On":
            # GPIO.output(SPRAY_PIN.LOW)  PIN25
            print("Spray",":", message)
        else :
            # GPIO.output(SPRAY_PIN.HIGH) PIN25
            print("Spray",":", message)
        
        response_msg = f"{device},{message}"
        try:
            
             # client.publish(topic, response_msg)
            publish_to_mongodb(device, message,client)
        except Exception as e:
            
            print("Error:", e)
          


               
        
def publish_pro1(client):
    publish(client)
    
def subscribe_pro2(client):
    subscribe(client)
    client.loop_forever()
    

    
def run():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup([PUMP_PIN,FERTILIZER_PIN, LIGHT_PIN], GPIO.OUT)

    client = connect_mqtt()
        
    p1 = multiprocessing.Process(target=publish_pro1,args=(client,)) 
    p2 = multiprocessing.Process(target=subscribe_pro2,args=(client,)) 
  
    # starting process 1 
    p1.start() 
    # starting process 2 
    p2.start() 
  
    # wait until process 1 is finished 
    p1.join() 
    # wait until process 2 is finished 
    p2.join() 
  
    # both processes finished 
   
    print("Done!") 
    
    
if __name__ == '__main__':
    run()

