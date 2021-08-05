import socket
import cv2
import pickle
import struct
import time
import imutils 
import pyttsx3 
import argparse
from stopwatch import Stopwatch

"""
Edits and comments by Fardin

1)  Added in arg parse so you don't have to change the camera varible in code everytime
    for so `python Camera-client.py --camera False` in the command line will play test_video.mp4

2) I commented out the speak() function to test.

3) I cleaned a few things here and there for example, line 63, There was some fuckery of turning ints
   into strings and back to ints. 

4) What is the point of the try catch block in line 114? YOu might want to double check that, since it overwrites the
   declaration of the `vid` variable. I commented it out since I wasn't using a camera. 

"""
# Argument Parser
def str2bool(v):
    """
    This is a helper function for the argument parser so that you can
    input booleans through the command line
    """
    if isinstance(v, bool):
        return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')


ap = argparse.ArgumentParser()
ap.add_argument("--camera", type=str2bool, nargs='?',
                const=True, default= False, help = 'Boolean for camera')
ap.add_argument("--host_ip", type=str, nargs='?',
                required = False, default= '127.0.0.1')
ap.add_argument("--port", type=str, nargs='?',
                required = False, default= 9999)
args = vars(ap.parse_args())


# Video stream
vid = cv2.VideoCapture(0) if args['camera'] else cv2.VideoCapture('test_video.mp4')

stop=Stopwatch()

# def speak(audio): 
#     """
#     Audio i/o

#     """
#     engine = pyttsx3.init()
#     engine.setProperty('rate', 130 )

#     voices = engine.getProperty('voices')
#     engine.setProperty('voice', voices[2].id)

#     engine.say(audio) 
#     engine.runAndWait() 


def sendData():

    VIOLATION_COUNT_SETTING = 2
    VIOLATION_TIME_SETTING = 6  
    VIOLATION_TIME_SETTING_2 = 10  
    stop.start()
    
    if client_socket:
        message = ["Room1",
                    400,
                    VIOLATION_COUNT_SETTING,
                    VIOLATION_TIME_SETTING,
                    VIOLATION_TIME_SETTING_2]
        
        a = pickle.dumps(message)
        message = struct.pack("Q", len(a)) + a
        client_socket.sendall(message)


    while vid.isOpened():
        try:
            img, frame = vid.read()
            frame = imutils.resize(frame, width=380)
            a = pickle.dumps(frame)
            message = struct.pack("Q", len(a)) + a
            client_socket.sendall(message)
            #print(stop.elapsed)
            #https://stackoverflow.com/questions/16745409/what-does-pythons-socket-recv-return-for-non-blocking-sockets-if-no-data-is-r

            msg = client_socket.recv(1024).decode()

            if msg == 'Violation':
                # speak("You are requested to Please Maintain Social Distancing")
                print('violation')

        except Exception as e:
            print('VIDEO FINISHED!', e)
            break

def connecttoServer():

    client_socket.connect((host_ip, port))
    print('Connected to the server')
    sendData()


if __name__ == '__main__':

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host_ip = args['host_ip']
    port = args['port']

    while True:
        if vid.isOpened():
            connecttoServer()
        else:
            print('Video closed')




