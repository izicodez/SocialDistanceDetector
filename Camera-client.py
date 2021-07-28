import socket,cv2, pickle,struct, time
#import pyshine as ps # pip install pyshine
import imutils # pip install imutils
from stopwatch import Stopwatch
import pyttsx3 #pip install pyttsx3



stop=Stopwatch()
camera = True


'''
if camera == True:
    #vid = cv2.VideoCapture('aa.mp4')
    vid = cv2.VideoCapture(0)
else:
    vid = cv2.VideoCapture('videos/mario.mp4')
'''
def speak(audio): # it will speak
    engine = pyttsx3.init()
    engine.setProperty('rate', 130 )

    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[2].id)

    engine.say(audio) # say the given audio
    engine.runAndWait() #Without this command, speech will not be audible to us.


def sendData():
    ###

    VIOLATION_COUNT_SETTING = 2
    VIOLATION_TIME_SETTING = 6  # Main message time
    VIOLATION_TIME_SETTING_2 = 10  # Spam him after .. minutes
    stop.start()
    ###
    if client_socket:
        message = ["Room1", 400, int(f"{VIOLATION_COUNT_SETTING}"), int(f"{VIOLATION_TIME_SETTING}"),
                   int(f"{VIOLATION_TIME_SETTING_2}")]
        # message=["Room1", 400,int(f"{VIOLATION_COUNT_SETTING}"),int(f"{VIOLATION_TIME_SETTING}")] #For original

        a = pickle.dumps(message)
        message = struct.pack("Q", len(a)) + a
        client_socket.sendall(message)


    while (vid.isOpened()):
        time.sleep(0.2)
        try:
            img, frame = vid.read()
            frame = imutils.resize(frame, width=380)
            a = pickle.dumps(frame)
            message = struct.pack("Q", len(a)) + a
            client_socket.sendall(message)
            #print(stop.elapsed)
#https://stackoverflow.com/questions/16745409/what-does-pythons-socket-recv-return-for-non-blocking-sockets-if-no-data-is-r

            msg = client_socket.recv(1024).decode()

            if (msg == "Violation"):
                speak("You are requested to Please Maintain Social Distancing")
                print('violation')

        except Exception as e:
            print('VIDEO FINISHED!', e)
            break

def connecttoServer():
    while True:
        try:
            client_socket.connect((host_ip, port))
            print('Connected to the server')
            sendData()

            break
        except:
            pass


while True:
    try:
        try:
            vid = cv2.VideoCapture(0)
            if vid is None or not vid.isOpened():
                vid = cv2.VideoCapture(1)
        except Exception as ex:
            print(ex)
            
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # host_ip = '127.0.0.1' # Here according to your server ip write the address
        host_ip = '192.168.152.99'
        port = 9999
        if vid.isOpened():
            connecttoServer()
        elif not vid.isOpened():
            print("Camera is disabled, Please Check")


        time.sleep(3)
    except:
        pass




