import paho.mqtt.client as mqtt
import serial
import time
import json
from datetime import datetime
import threading
from threading import Event



# MQTT configuration
mqtt_broker_address = "localhost"
mqtt_topic_serial = "serial_data"
b1_mqtt_log_1015 = "b1_log_data_1015"
b1_mqtt_log_1115 = "b1_log_data_1115"
b2_mqtt_log_1015 = "b2_log_data_1015"
b2_mqtt_log_1115 = "b2_log_data_1115"
b3_mqtt_log_1015 = "b3_log_data_1015"
b3_mqtt_log_1115 = "b3_log_data_1115"
b4_mqtt_log_1015 = "b4_log_data_1015"
b4_mqtt_log_1115 = "b4_log_data_1115"
b5_mqtt_log_1015 = "b5_log_data_1015"
b5_mqtt_log_1115 = "b5_log_data_1115"

mqtt_switch_states_update = "switch_states_update"
mqtt_switch_states_status = "switch_states_status"


with open('cf_config.json', 'r') as json_file:
    conv_configs = json.load(json_file)

cf_1015 = conv_configs['Conv_Factor_ADS1015']
cf_1115 = conv_configs['Conv_Factor_ADS1115']


client = mqtt.Client("propdaq")

ports = [False, False, False, False, False]

def open_serial_ports():
    try:
        ports[0] = serial.Serial('/dev/cu.usbserial-0001', 921600)  
    except Exception as e:
            print(f"Port error: {e}")
        
    try:
        ports[1] = serial.Serial('/dev/cu.usbserial-1', 921600)  
    except Exception as e:
            print(f"Port error: {e}")
    
    try:
        ports[2] = serial.Serial('/dev/cu.usbserial-3', 921600)  
    except Exception as e:
            print(f"Port error: {e}")


# Open a text file for appending
gui_log_file = open('gui_serial.txt', 'w')
raw_log_file = open('raw_serial_log.txt', 'a')
raw_log_file_2 = open('raw_serial_log_2.txt', 'a')
raw_log_file_3 = open('raw_serial_log_3.txt', 'a')
raw_log_file_4 = open('raw_serial_log_4.txt', 'a')
raw_log_file_5 = open('raw_serial_log_5.txt', 'a')

event = Event()
read_event = Event()

datatopass = ["", "", "", ""]
datatopass2 = ["", "", "", ""]
datatopass3 = ["", "", "", ""]
datatopass4 = ["", "", "", ""]
datatopass5 = ["", "", "", ""]
data_lock = threading.Lock()


def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT broker with result code "+str(rc))
    client.subscribe(mqtt_topic_serial)
    client.subscribe(mqtt_switch_states_update)
    

def on_message(client, userdata, message):
    print(f"Received message on topic '{message.topic}': {message.payload.decode('utf-8')}")
    command = message.payload.decode('utf-8')
    if (message.topic == "switch_states_update"):
        print(command)
        ports[0].read_all()  # Read one line (you can also use ser.read() for binary data)
        ports[0].write(command.encode())
        print("Command sent:", command)


def read_serial_and_log_high_freq_1():
    while True:
        try:
            # Read a line of data from the Serial Monitor
            data = ports[0].readline().decode('utf-8').strip()
            data_dict = json.loads(data)

            datatopass[3] = data_dict['BoardID']
            
            #print(data_dict)
            # Log the data to a text file
            
            data_formatted = (
                str(datetime.now())[11:] 
                + " "
                + str(data_dict['BoardID'])
                + "  "
                + str(data_dict['SensorType'])
                + "  ")
            for i in range(len(data_dict['Sensors'])):
                data_formatted += str(data_dict['Sensors'][i]) + "  "
            
            #print (data_formatted)
            #print (publish_json)
            #print(data_dict)
            #print (datatopass)                
            
            with data_lock:
                datatopass[0] = data_formatted
                datatopass[1] = data_dict['SensorType']
                publish_json = (
                "{\"time\": \"" + str(datetime.now())[11:22] 
                + "\","
                + "\"sensor_readings\": "
                )
                converted_values = []
                for i in range(len(data_dict['Sensors'])):
                    if datatopass[1] == 'ADS1015':
                        converted_values.append(round(data_dict['Sensors'][i] * cf_1015, 1))
                    else:
                        converted_values.append(round(data_dict['Sensors'][i] * cf_1115, 1))
            
                publish_json += str(converted_values)
                publish_json += '}'
                datatopass[2] = publish_json
                raw_log_file.write(data_formatted)
                raw_log_file.flush()  # Flush the buffer to ensure data is written immediately

        except Exception as e:
            print(f"Serial read error: {e}")

    #, {data}")



def read_serial_and_log_high_freq_2():
    while True:
        try:
            # Read a line of data from the Serial Monitor
            data = ports[1].readline().decode('utf-8').strip()
            data_dict = json.loads(data)


            datatopass2[3] = data_dict['BoardID']
            
            #print(data_dict)
            # Log the data to a text file
            
            data_formatted = (
                str(datetime.now())[11:] 
                + " "
                + str(data_dict['BoardID'])
                + "  "
                + str(data_dict['SensorType'])
                + "  ")
            for i in range(len(data_dict['Sensors'])):
                data_formatted += str(data_dict['Sensors'][i]) + "  "
            
            #print (data_formatted)
            #print (publish_json)
            #print(data_dict)
            #print (datatopass)                
            
            with data_lock:
                datatopass2[0] = data_formatted
                datatopass2[1] = data_dict['SensorType']
                publish_json = (
                "{\"time\": \"" + str(datetime.now())[11:22] 
                + "\","
                + "\"sensor_readings\": "
                )
                converted_values = []
                for i in range(len(data_dict['Sensors'])):
                    if datatopass2[1] == 'ADS1015':
                        converted_values.append(round(data_dict['Sensors'][i] * cf_1015, 1))
                    else:
                        converted_values.append(round(data_dict['Sensors'][i] * cf_1115, 1))
            
                publish_json += str(converted_values)
                publish_json += '}'
                datatopass2[2] = publish_json
                raw_log_file_2.write(data_formatted)
                raw_log_file_2.flush()  # Flush the buffer to ensure data is written immediately

        except Exception as e:
            print(f"Serial read error: {e}")
            #, {data}") 


def read_serial_and_log_high_freq_3():
    while True:
        try:
            # Read a line of data from the Serial Monitor
            data = ports[2].readline().decode('utf-8').strip()
            data_dict = json.loads(data)


            datatopass3[3] = data_dict['BoardID']
            
            #print(data_dict)
            # Log the data to a text file
            
            data_formatted = (
                str(datetime.now())[11:] 
                + " "
                + str(data_dict['BoardID'])
                + "  "
                + str(data_dict['SensorType'])
                + "  ")
            for i in range(len(data_dict['Sensors'])):
                data_formatted += str(data_dict['Sensors'][i]) + "  "
            
            #print (data_formatted)
            #print (publish_json)
            #print(data_dict)
            #print (datatopass)                
            
            with data_lock:
                datatopass3[0] = data_formatted
                datatopass3[1] = data_dict['SensorType']
                publish_json = (
                "{\"time\": \"" + str(datetime.now())[11:22] 
                + "\","
                + "\"sensor_readings\": "
                )
                converted_values = []
                for i in range(len(data_dict['Sensors'])):
                    if datatopass3[1] == 'ADS1015':
                        converted_values.append(round(data_dict['Sensors'][i] * cf_1015, 1))
                    else:
                        converted_values.append(round(data_dict['Sensors'][i] * cf_1115, 1))
            
                publish_json += str(converted_values)
                publish_json += '}'
                datatopass3[2] = publish_json
                raw_log_file_3.write(data_formatted)
                raw_log_file_3.flush()  # Flush the buffer to ensure data is written immediately

        except Exception as e:
            print(f"Serial read error: {e}")
            #, {data}") 


def read_serial_and_log_high_freq_4():
    while True:
        try:
            # Read a line of data from the Serial Monitor
            data = ports[3].readline().decode('utf-8').strip()
            data_dict = json.loads(data)


            datatopass4[3] = data_dict['BoardID']
            
            #print(data_dict)
            # Log the data to a text file
            
            data_formatted = (
                str(datetime.now())[11:] 
                + " "
                + str(data_dict['BoardID'])
                + "  "
                + str(data_dict['SensorType'])
                + "  ")
            for i in range(len(data_dict['Sensors'])):
                data_formatted += str(data_dict['Sensors'][i]) + "  "
            
            #print (data_formatted)
            #print (publish_json)
            #print(data_dict)
            #print (datatopass)                
            
            with data_lock:
                datatopass4[0] = data_formatted
                datatopass4[1] = data_dict['SensorType']
                publish_json = (
                "{\"time\": \"" + str(datetime.now())[11:22] 
                + "\","
                + "\"sensor_readings\": "
                )
                converted_values = []
                for i in range(len(data_dict['Sensors'])):
                    if datatopass4[1] == 'ADS1015':
                        converted_values.append(round(data_dict['Sensors'][i] * cf_1015, 1))
                    else:
                        converted_values.append(round(data_dict['Sensors'][i] * cf_1115, 1))
            
                publish_json += str(converted_values)
                publish_json += '}'
                datatopass4[2] = publish_json
                raw_log_file_4.write(data_formatted)
                raw_log_file_4.flush()  # Flush the buffer to ensure data is written immediately

        except Exception as e:
            print(f"Serial read error: {e}")
            #, {data}") 


def read_serial_and_log_high_freq_5():
    while True:
        try:
            # Read a line of data from the Serial Monitor
            data = ports[4].readline().decode('utf-8').strip()
            data_dict = json.loads(data)


            datatopass4[3] = data_dict['BoardID']
            
            #print(data_dict)
            # Log the data to a text file
            
            data_formatted = (
                str(datetime.now())[11:] 
                + " "
                + str(data_dict['BoardID'])
                + "  "
                + str(data_dict['SensorType'])
                + "  ")
            for i in range(len(data_dict['Sensors'])):
                data_formatted += str(data_dict['Sensors'][i]) + "  "
            
            #print (data_formatted)
            #print (publish_json)
            #print(data_dict)
            #print (datatopass)                
            
            with data_lock:
                datatopass4[0] = data_formatted
                datatopass4[1] = data_dict['SensorType']
                publish_json = (
                "{\"time\": \"" + str(datetime.now())[11:22] 
                + "\","
                + "\"sensor_readings\": "
                )
                converted_values = []
                for i in range(len(data_dict['Sensors'])):
                    if datatopass4[1] == 'ADS1015':
                        converted_values.append(round(data_dict['Sensors'][i] * cf_1015, 1))
                    else:
                        converted_values.append(round(data_dict['Sensors'][i] * cf_1115, 1))
            
                publish_json += str(converted_values)
                publish_json += '}'
                datatopass4[2] = publish_json
                raw_log_file_4.write(data_formatted)
                raw_log_file_4.flush()  # Flush the buffer to ensure data is written immediately

        except Exception as e:
            print(f"Serial read error: {e}")
            #, {data}") 
            

def publish_data_1():
    while True:
        time.sleep(0.05)
        board_topic_1015 = ""
        board_topic_1115 = ""
        if (datatopass[3] == "Board 1"):
            board_topic_1015 = b1_mqtt_log_1015
            board_topic_1115 = b1_mqtt_log_1115
        elif (datatopass[3] == "Board 2"):
            board_topic_1015 = b2_mqtt_log_1015
            board_topic_1115 = b2_mqtt_log_1115
        elif (datatopass[3] == "Board 3"):
            board_topic_1015 = b3_mqtt_log_1015
            board_topic_1115 = b3_mqtt_log_1115
        elif (datatopass[3] == "Board 4"):
            board_topic_1015 = b4_mqtt_log_1015
            board_topic_1115 = b4_mqtt_log_1115
        elif (datatopass[3] == "Board 5"):
            board_topic_1015 = b5_mqtt_log_1015
            board_topic_1115 = b5_mqtt_log_1115

        with data_lock:
            if datatopass[1] == 'ADS1015':
                client.publish(board_topic_1015, datatopass[2])
                #print(datatopass)
            if datatopass[1] == 'ADS1115':
                client.publish(board_topic_1115, datatopass[2])
                #print(datatopass)


def publish_data_2():
    while True:
        time.sleep(0.05)
        board_topic_1015 = ""
        board_topic_1115 = ""
        if (datatopass2[3] == "Board 1"):
            board_topic_1015 = b1_mqtt_log_1015
            board_topic_1115 = b1_mqtt_log_1115
        elif (datatopass2[3] == "Board 2"):
            board_topic_1015 = b2_mqtt_log_1015
            board_topic_1115 = b2_mqtt_log_1115
        elif (datatopass2[3] == "Board 3"):
            board_topic_1015 = b3_mqtt_log_1015
            board_topic_1115 = b3_mqtt_log_1115
        elif (datatopass2[3] == "Board 4"):
            board_topic_1015 = b4_mqtt_log_1015
            board_topic_1115 = b4_mqtt_log_1115
        elif (datatopass2[3] == "Board 5"):
            board_topic_1015 = b5_mqtt_log_1015
            board_topic_1115 = b5_mqtt_log_1115

        with data_lock:
            if datatopass2[1] == 'ADS1015':
                client.publish(board_topic_1015, datatopass2[2])
                #print(datatopass)
            if datatopass2[1] == 'ADS1115':
                client.publish(board_topic_1115, datatopass2[2])
                #print(datatopass)


def publish_data_3():
    while True:
        time.sleep(0.05)
        board_topic_1015 = ""
        board_topic_1115 = ""
        if (datatopass3[3] == "Board 1"):
            board_topic_1015 = b1_mqtt_log_1015
            board_topic_1115 = b1_mqtt_log_1115
        elif (datatopass3[3] == "Board 2"):
            board_topic_1015 = b2_mqtt_log_1015
            board_topic_1115 = b2_mqtt_log_1115
        elif (datatopass3[3] == "Board 3"):
            board_topic_1015 = b3_mqtt_log_1015
            board_topic_1115 = b3_mqtt_log_1115
        elif (datatopass3[3] == "Board 4"):
            board_topic_1015 = b4_mqtt_log_1015
            board_topic_1115 = b4_mqtt_log_1115
        elif (datatopass3[3] == "Board 5"):
            board_topic_1015 = b5_mqtt_log_1015
            board_topic_1115 = b5_mqtt_log_1115

        with data_lock:
            if datatopass3[1] == 'ADS1015':
                client.publish(board_topic_1015, datatopass3[2])
                #print(datatopass)
            if datatopass3[1] == 'ADS1115':
                client.publish(board_topic_1115, datatopass3[2])
                #print(datatopass)


def publish_data_4():
    while True:
        time.sleep(0.05)
        board_topic_1015 = ""
        board_topic_1115 = ""
        if (datatopass4[3] == "Board 1"):
            board_topic_1015 = b1_mqtt_log_1015
            board_topic_1115 = b1_mqtt_log_1115
        elif (datatopass4[3] == "Board 2"):
            board_topic_1015 = b2_mqtt_log_1015
            board_topic_1115 = b2_mqtt_log_1115
        elif (datatopass4[3] == "Board 3"):
            board_topic_1015 = b3_mqtt_log_1015
            board_topic_1115 = b3_mqtt_log_1115
        elif (datatopass4[3] == "Board 4"):
            board_topic_1015 = b4_mqtt_log_1015
            board_topic_1115 = b4_mqtt_log_1115
        elif (datatopass4[3] == "Board 5"):
            board_topic_1015 = b5_mqtt_log_1015
            board_topic_1115 = b5_mqtt_log_1115

        with data_lock:
            if datatopass4[1] == 'ADS1015':
                client.publish(board_topic_1015, datatopass4[2])
                #print(datatopass)
            if datatopass4[1] == 'ADS1115':
                client.publish(board_topic_1115, datatopass4[2])
                #print(datatopass)


def publish_data_5():
    while True:
        time.sleep(0.05)
        board_topic_1015 = ""
        board_topic_1115 = ""
        if (datatopass5[3] == "Board 1"):
            board_topic_1015 = b1_mqtt_log_1015
            board_topic_1115 = b1_mqtt_log_1115
        elif (datatopass5[3] == "Board 2"):
            board_topic_1015 = b2_mqtt_log_1015
            board_topic_1115 = b2_mqtt_log_1115
        elif (datatopass5[3] == "Board 3"):
            board_topic_1015 = b3_mqtt_log_1015
            board_topic_1115 = b3_mqtt_log_1115
        elif (datatopass5[3] == "Board 4"):
            board_topic_1015 = b4_mqtt_log_1015
            board_topic_1115 = b4_mqtt_log_1115
        elif (datatopass5[3] == "Board 5"):
            board_topic_1015 = b5_mqtt_log_1015
            board_topic_1115 = b5_mqtt_log_1115

        with data_lock:
            if datatopass5[1] == 'ADS1015':
                client.publish(board_topic_1015, datatopass5[2])
                #print(datatopass)
            if datatopass5[1] == 'ADS1115':
                client.publish(board_topic_1115, datatopass5[2])
                #print(datatopass)
            

def main():
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(mqtt_broker_address, 1883, 60)
    client.loop_start()

    open_serial_ports()


    t1 = threading.Thread(target=read_serial_and_log_high_freq_1)
    t2 = threading.Thread(target=read_serial_and_log_high_freq_2)
    t3 = threading.Thread(target=read_serial_and_log_high_freq_3)
    t4 = threading.Thread(target=read_serial_and_log_high_freq_4)
    t5 = threading.Thread(target=read_serial_and_log_high_freq_5)



    t6 = threading.Thread(target=publish_data_1)
    t7 = threading.Thread(target=publish_data_2)
    t8 = threading.Thread(target=publish_data_3)
    t9 = threading.Thread(target=publish_data_4)
    t10 = threading.Thread(target=publish_data_5)


    if (ports[0]):
        t1.start()
        t6.start()

    if (ports[1]):
        t2.start()
        t7.start()

    if (ports[2]):
        t3.start()
        t8.start()
    
    if (ports[3]):
        t4.start()
        t9.start()
    
    if (ports[4]):
        t5.start()
        t10.start()
    

if __name__ == '__main__':
    main()
