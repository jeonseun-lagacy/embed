import Adafruit_DHT
import bluetooth
import time
import requests

#Send module
bd_addr = "DC:A6:32:96:16:89"
sensor = Adafruit_DHT.DHT22
port = 1
pin=18
count = 30


def dataToWeb(data, data2):
    print("data log send to web application server")

    url = 'localhost'
    id = "test1"

    try:
        # 현재시간 정보 
        now = time.localtime()
        now_time = "%04d-%02d-%02d %02d:%02d:%02d" % (now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min, now.tm_sec)

        web_data = "{'id' : '%s', 'time' : '%s', 'temperature' : '%s' , 'humidity' : '%s'}"%(id, now_time,str(data), str(data2))

        r = requests.post('http://%s:8080/temperature'%url, json=web_data)
        
    except Exception as e:
        print(e)

if __name__ == "__main__":
    try:
        while(1):
            sock=bluetooth.BluetoothSocket(bluetooth.RFCOMM)
            sock.connect((bd_addr, port))
            humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)

            if count == 30:
                count = 0
                dataToWeb(temperature, humidity)
    
            if humidity is not None and temperature is not None:
                print('Temp={0:0.1f}*C Humidity={1:0.1f}%'.format(temperature, humidity))
                sock.send((str(temperature)))
            else:
                print('Failed to get reading. Try again!')
            sock.close()
            time.sleep(60)
            count = count + 1
    except:
        sock.close()
        
