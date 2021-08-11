import socket,cv2, pickle,struct, time
#import pyshine as ps # pip install pyshine
import imutils # pip install imutils
from stopwatch import Stopwatch
stop=Stopwatch()
camera = True
if camera == True:
    vid = cv2.VideoCapture('a.mp4')
else:
    vid = cv2.VideoCapture('videos/mario.mp4')
client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
host_ip = '127.0.0.1' # Here according to your server ip write the address

port = 9999
while True:
    try:
        client_socket.connect((host_ip,port))
        break
    except:
        pass

###
VIOLATION_COUNT_SETTING=2
VIOLATION_TIME_SETTING=5   #Main message time
VIOLATION_TIME_SETTING_2=10 #Spam him after .. minutes
stop.start()
###
if client_socket:
    message=["Room2", 50,int(f"{VIOLATION_COUNT_SETTING}"),int(f"{VIOLATION_TIME_SETTING}"),int(f"{VIOLATION_TIME_SETTING_2}")]
    #message=["Room1", 400,int(f"{VIOLATION_COUNT_SETTING}"),int(f"{VIOLATION_TIME_SETTING}")] #For original

    a = pickle.dumps(message)
    message = struct.pack("Q",len(a))+a
    client_socket.sendall(message)
	
while (vid.isOpened()):
    time.sleep(0.2)
    try:
        img, frame = vid.read()
        frame = imutils.resize(frame,width=380)
        a = pickle.dumps(frame)
        message = struct.pack("Q",len(a))+a
        client_socket.sendall(message)
        print(stop.elapsed)

        
    except:
        print('VIDEO FINISHED!')
        break
