import bluetooth
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
leds = [18, 23, 24]
ledStates = [0, 0, 0]
season = ["summer", "winter"]
summer_temperture = [24, 26, 28, 30]
winter_temperture = [16, 18, 20, 22]
led_status_info = ["green", "yellow", "red"]

season_status = season[0]
led_status = "init"
status_flag = "init"

server_sock=bluetooth.BluetoothSocket(bluetooth.RFCOMM)

port = 1
server_sock.bind(("",port))
server_sock.listen(1)

GPIO.setup(leds[0], GPIO.OUT)
GPIO.setup(leds[1], GPIO.OUT)
GPIO.setup(leds[2], GPIO.OUT)

def summer_control():
    led_status = status_flag
    all_off()

    if(led_status == led_status_info[0]):
        green_on()
    elif(led_status == led_status_info[1]):
        yellow_on()
    elif(led_status == led_status_info[2]):
        red_on()



def all_off():
    GPIO.output(18, False)
    GPIO.output(23, False)
    GPIO.output(24, False)

def green_on():
    GPIO.output(18, True)

def yellow_on():
    GPIO.output(23, True)

def red_on():
    GPIO.output(24, True)

if __name__ == "__main__":
    try: 
        while 1:
            client_sock,address = server_sock.accept()
            print ("Accepted connection from ",address)
    
            data = client_sock.recv(1024)
            print ("received [%s]" % data)

            if(season_status == "summer"):
                if(float(data) < summer_temperture[0]):
                    status_flag = led_status_info[2]
                elif(float(data) > summer_temperture[0] and float(data) < summer_temperture[1]):
                    status_flag = led_status_info[1]
                elif(float(data) > summer_temperture[1] and float(data) < summer_temperture[2]):
                    status_flag = led_status_info[0]
                elif(float(data) > summer_temperture[2] and float(data) < summer_temperture[3]):
                    status_flag = led_status_info[1]
                elif(float(data) > summer_temperture[3]):
                    status_flag = led_status_info[2]

                if(led_status != status_flag):
                    summer_control()

    except:
        client_sock.close()
        server_sock.close()
