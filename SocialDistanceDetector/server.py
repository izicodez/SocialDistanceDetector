import socket
import cv2
import pickle
import struct
import imutils
import threading
import time
import datetime
import random
import argparse
import os
import numpy as np
from time import sleep
from datetime import date
from scipy.spatial import distance as dist
from stopwatch import Stopwatch, profile

#Formerly named nomi_izi
from sd_utils import social_distancing_config as config
from sd_utils.detection import detect_boxes
# Commented out to make testing easier
#from whatsapp import send_violation_picture,send_message

'''
Edits by Fardin:

I made a few changes.

Mostly just to make code cleaner. Many variables were declared many times.
There was some str -> int -> str fuckery

It's working as intended for me.

'''

# Argument parser
ap = argparse.ArgumentParser()
ap.add_argument('-i', '--input', type=str, default='',
                help='path to (optional) input video file')
ap.add_argument('-o', '--output', type=str, default='',
                help='path to (optional) output video file')
ap.add_argument('-d', '--display', type=int, default=1,
                help='whether or not output frame should be displayed')
ap.add_argument('--host_ip', type=str, required = False,
                 default= '127.0.0.1')
ap.add_argument('--port', type=str,required = False,
                 default= 9999)
args = vars(ap.parse_args())

# Server settings
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host_name = socket.gethostname()
host_ip = args['host_ip']
port = args['port']

print(f'HOST IP: {host_ip}')
socket_address = (host_ip, port)
server_socket.bind(socket_address)
server_socket.listen()
print(f'Listening at {socket_address}')

count = 0

def show_client(addr, client_socket, lock):

    #Load yolo model, set backend device and NN initialize layers
    print('[INFO] loading YOLO from disk...')
    labelsPath = os.path.sep.join(['yolo-coco', 'coco.names'])
    LABELS = open(labelsPath).read().strip().split('\n')
    weightsPath = os.path.sep.join(['yolo-coco', 'yolov3.weights'])
    configPath = os.path.sep.join(['yolo-coco', 'yolov3.cfg'])
    net = cv2.dnn.readNetFromDarknet(configPath, weightsPath)

    if config.USE_GPU:
        print('[INFO] setting preferable backend and target to CUDA...')
        net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
        net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)

    ln = net.getLayerNames()
    ln = [ln[i[0] - 1] for i in net.getUnconnectedOutLayers()]
    writer = None

    # Recieve data from client
    data = b''
    payload_size = struct.calcsize('Q')
    while len(data) < payload_size:
        packet = client_socket.recv(4*1024) 
        if not packet:
            break
        data += packet

    # Recieve frames
    packed_msg_size = data[:payload_size]
    data = data[payload_size:]
    msg_size = struct.unpack('Q', packed_msg_size)[0]
    while len(data) < msg_size:
        data += client_socket.recv(4*1024)

    frame_data = data[:msg_size]
    data = data[msg_size:]
    config_list = pickle.loads(frame_data)
    print(config_list)
    
    # Configuration data from client file
    ROOM_NAME,MIN_DISTANCE,\
    VIOLATION_COUNT_SETTING,\
    VIOLATION_TIME_SETTING,\
    VIOLATION_TIME_SETTING_2 = tuple(config_list)

    print(f'\n\nCamera connected with $$ {ROOM_NAME} $$ Successfully\n\n')

    stopwatch=Stopwatch()
    engine=True
    stopwatch2=Stopwatch()
    engine2=True
    timeCounter=0
    
    try:
        if client_socket:  
            print(f'CLIENT {addr} CONNECTED!')

            while True:
                msg = b'Thank you for connecting'
                client_socket.send(msg)
                time.sleep(0.20)
                while len(data) < payload_size:
                    packet = client_socket.recv(4*1024) 
                    if not packet:
                        break
                    data += packet

                packed_msg_size = data[:payload_size]
                data = data[payload_size:]
                msg_size = struct.unpack('Q', packed_msg_size)[0]
                while len(data) < msg_size:
                    data += client_socket.recv(4*1024)
                frame_data = data[:msg_size]
                data = data[msg_size:]
                frame = pickle.loads(frame_data)
                frame = imutils.resize(frame, width=700)


                results = detect_boxes(frame, net, ln,
                                        personIdx=LABELS.index('person'))

                #set of violations indexes, MIGHT wanna double check data structure
                violate = set()

                if len(results) >= 2:
                    centroids = np.array([r[2] for r in results])
                    D = dist.cdist(centroids, centroids, metric='euclidean')

  
                    for i in range(0, D.shape[0]):
                        for j in range(i + 1, D.shape[1]):
                            if D[i, j] < MIN_DISTANCE:
                                violate.add(i)
                                violate.add(j)


                for (i, (prob, bbox, centroid)) in enumerate(results):
                    (startX, startY, endX, endY) = bbox
                    (cX, cY) = centroid
                    color = (0, 0, 255) if i in violate else (0, 255, 0)

                    cv2.rectangle(frame, (startX, startY),
                                  (endX, endY), color, 2)
                    cv2.circle(frame, (cX, cY), 5, color, 1)

                violation_count= len(violate)
                text = f'Social Distancing Violations: {violation_count}'
                cv2.putText(frame, text, (10, frame.shape[0] - 25),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.85, (0, 0, 255), 3)


                if args['display'] > 0:
                    name = f'Frame_ {ROOM_NAME} {count}'
                    cv2.imshow(name, frame)
                    key = cv2.waitKey(1) & 0xFF

                    # if key == ord('q'):
                    #     break

                # if an output video file path has been supplied and the video
                # writer has not been initialized, do so now
                if args['output'] != '' and writer is None:
                    fourcc = cv2.VideoWriter_fourcc(*'MJPG')
                    writer = cv2.VideoWriter(args['output'], fourcc, 25,
                                            (frame.shape[1], frame.shape[0]), True)


                if writer is not None:
                    writer.write(frame)

                if not engine:
                    print(f'{round(stopwatch.elapsed,1)}, seconds')

#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

# BRUH

#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

                if violation_count >= VIOLATION_COUNT_SETTING:
                    print(f'{len(results)}, detected.')
                    if engine:
                        stopwatch = Stopwatch()
                        stopwatch.start()
                        print(f'time {stopwatch.elapsed}')
                        engine = 0


                        
                    if stopwatch.elapsed > VIOLATION_TIME_SETTING and engine2:

                        violation_count,people = len(violate),len(results)
                        datee = datetime.datetime.now()\
                        .strftime('%D %T').replace(':','-').replace('/','-')
                        print(datee)

                        violation_console_output = f'Total Violations: {violation_count}.'\
                                                   f' Total People: {people}'\
                                                   f'\nViolations are detected at location: {ROOM_NAME}.'

                        violation_picture_path =   f'violation_log/Room1/pic {ROOM_NAME} {datee}.jpg'

                        msg = b'Violation'
                        client_socket.send(msg)
                        stopwatch2=Stopwatch()
                        stopwatch2.start()

                        print(violation_console_output)

                        cv2.imwrite(violation_picture_path, frame)

                        msg= f'{violation_count} violations detected out of {people}'\
                             f' people in {ROOM_NAME} on {datee}. Please Check.'
                        # send_violation_picture(lock,
                        #      violation_picture_path,msg)

                        engine = 1
                        engine2 = 0
                        stopwatch.stop()
                        print(f'time {stopwatch.elapsed} {engine2}')

                    elif stopwatch2.elapsed > VIOLATION_TIME_SETTING_2:

                        timeCounter += 1
                        print(f'stp2 ---- {stopwatch2.elapsed:.2f} seconds'\
                               ' still happening')

                        stopwatch2=Stopwatch()
                        stopwatch2.start()
                        people,violation_count = len(results),len(violate)
                        msg=f'{violation_count} violations are still detected out of {people}'\
                            f' people in {ROOM_NAME} on {datee} for {timeCounter*2} Minutes.'\
                             ' Please Check Immediately.'
                        # send_message(lock, msg)  #256, 270
                        # send_violation_picture(lock,
                        #      violation_picture_path,msg)
                        
                        # send_message(lock, msg)

                #else if(not engine2 and stopwatch2.elapsed == 0):
                    
                else:
                    if stopwatch.elapsed !=0:
                        # msg='Violation Has been cleared! No need to go.'
                        # send_message(lock, msg)
                        # VIOLATION_TIME_SETTING  config_list[3]
                        timeCounter=0
                        engine=True
                        engine2=True
                        stopwatch.stop()
                        stopwatch2.stop()
                        print('------------------------------RESET!!!!!!!')
                        
                    # if engine2:
                    #     msg='Violation Has been cleared! No need to go.'
                    #     send_message(lock, msg)
                    #     engine2=False

            client_socket.close()
            print('CLOSING SOCKET')
    except Exception as e:
        print(f'CLINET {addr} DISCONNECTED')
        print(e)
        pass

if __name__ == '__main__':

    lock=threading.Lock()
    while True:
        client_socket, addr = server_socket.accept()
        count +=1
        #id = random.randint(1,1000)
        thread = threading.Thread(target=show_client, args=(addr, client_socket, lock))
        thread.start()
        #thread.join()
        print(f'TOTAL CLIENTS {threading.activeCount() - 1}')
