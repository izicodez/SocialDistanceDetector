import socket
import cv2
import pickle
import struct
import imutils
import threading
# import pyshine as ps # pip install pyshine
import cv2
##################
from datetime import date
import datetime
import tkinter
from tkinter import *
import cv2
import PIL.Image, PIL.ImageTk
import time
from nomi_izi import social_distancing_config as config
from nomi_izi.detection import detect_people
from scipy.spatial import distance as dist
import numpy as np
import argparse
import time
import cv2
import os
import imutils
from tkinter import Tk, Label, font
from time import sleep
####################

from stopwatch import Stopwatch, profile
import time
##################
from whatsapp import send_violation_picture,send_message
################
# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--input", type=str, default="",
	help="path to (optional) input video file")
ap.add_argument("-o", "--output", type=str, default="",
	help="path to (optional) output video file")
ap.add_argument("-d", "--display", type=int, default=1,
	help="whether or not output frame should be displayed")
args = vars(ap.parse_args())

# load the COCO class labels our YOLO model was trained on
labelsPath = os.path.sep.join(["yolo-coco", "coco.names"])
LABELS = open(labelsPath).read().strip().split("\n")

# derive the paths to the YOLO weights and model configuration
weightsPath = os.path.sep.join(["yolo-coco", "yolov3.weights"])
configPath = os.path.sep.join(["yolo-coco", "yolov3.cfg"])

# load our YOLO object detector trained on COCO dataset (80 classes)
print("[INFO] loading YOLO from disk...")
net = cv2.dnn.readNetFromDarknet(configPath, weightsPath)

# check if we are going to use GPU
#if config.USE_GPU:
if True:
	# set CUDA as the preferable backend and target
	print("[INFO] setting preferable backend and target to CUDA...")
	net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
	net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)

# determine only the *output* layer names that we need from YOLO
ln = net.getLayerNames()
ln = [ln[i[0] - 1] for i in net.getUnconnectedOutLayers()]

# initialize the video stream and pointer to output video file
print("[INFO] accessing video stream...")



##################
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host_name = socket.gethostname()
#host_ip = socket.gethostbyname(host_name)
host_ip = '127.0.0.1'
print('HOST IP:', host_ip)
port = 9999
socket_address = (host_ip, port)
server_socket.bind(socket_address)
server_socket.listen()
print("Listening at", socket_address)


def show_client(addr, client_socket, lock):
    stopwatch=Stopwatch()
    
    data = b""
    payload_size = struct.calcsize("Q")
    writer = None
    while len(data) < payload_size:
        packet = client_socket.recv(4*1024)  # 4K
        if not packet:
            break
        data += packet
    packed_msg_size = data[:payload_size]
    data = data[payload_size:]
    msg_size = struct.unpack("Q", packed_msg_size)[0]

    while len(data) < msg_size:
        data += client_socket.recv(4*1024)
    frame_data = data[:msg_size]
    data = data[msg_size:]
    LIST = pickle.loads(frame_data)
    print(LIST)
    #$$$$$$$
    ROOM_NAME=LIST[0]
    MIN_DISTANCE=LIST[1]
    VIOLATION_COUNT_SETTING=LIST[2]
    VIOLATION_TIME_SETTING=LIST[3]
    #$$$$$$$
    print("\n\nCamera connected with $$ ", ROOM_NAME, " $$ Successfully\n\n")
    engine=True
    engine2=False
    
    try:
        print('CLIENT {} CONNECTED!'.format(addr))
        if client_socket:  # if a client socket exists
            
            while True:
                while len(data) < payload_size:
                    packet = client_socket.recv(4*1024)  # 4K
                    if not packet:
                        break
                    data += packet
                packed_msg_size = data[:payload_size]
                data = data[payload_size:]
                msg_size = struct.unpack("Q", packed_msg_size)[0]

                while len(data) < msg_size:
                    data += client_socket.recv(4*1024)
                frame_data = data[:msg_size]
                data = data[msg_size:]
                frame = pickle.loads(frame_data)
                frame = imutils.resize(frame, width=700)

                # resize the frame and then detect people (and only people) in it
                frame = imutils.resize(frame, width=700)
                results = detect_people(frame, net, ln,
                                        personIdx=LABELS.index("person"))

                # initialize the set of indexes that violate the minimum social
                # distance
                violate = set()

                # ensure there are *at least* two people detections (required in
                # order to compute our pairwise distance maps)
                if len(results) >= 2:
                    # extract all centroids from the results and compute the
                    # Euclidean distances between all pairs of the centroids
                    centroids = np.array([r[2] for r in results])
                    D = dist.cdist(centroids, centroids, metric="euclidean")

                    # loop over the upper triangular of the distance matrix
                    for i in range(0, D.shape[0]):
                        for j in range(i + 1, D.shape[1]):
                            # check to see if the distance between any two
                            # centroid pairs is less than the configured number
                            # of pixels
                            if D[i, j] < MIN_DISTANCE:
                                # update our violation set with the indexes of
                                # the centroid pairs
                                violate.add(i)
                                violate.add(j)

                # loop over the results
                for (i, (prob, bbox, centroid)) in enumerate(results):
                    # extract the bounding box and centroid coordinates, then
                    # initialize the color of the annotation
                    (startX, startY, endX, endY) = bbox
                    (cX, cY) = centroid
                    color = (0, 255, 0)

                    # if the index pair exists within the violation set, then
                    # update the color
                    if i in violate:
                        color = (0, 0, 255)

                    # draw (1) a bounding box around the person and (2) the
                    # centroid coordinates of the person,
                    cv2.rectangle(frame, (startX, startY),
                                  (endX, endY), color, 2)
                    cv2.circle(frame, (cX, cY), 5, color, 1)

                # draw the total number of social distancing violations on the
                # output frame
                #text = "Social Distancing Violations: {}".format(len(violate))
                #cv2.putText(frame, text, (10, frame.shape[0] - 25),
                #            cv2.FONT_HERSHEY_SIMPLEX, 0.85, (0, 0, 255), 3)

                # check to see if the output frame should be displayed to our
                # screen
                if args["display"] > 0:
                    # show the output frame
                    cv2.imshow("Frame", frame)
                    key = cv2.waitKey(1) & 0xFF

                    # if the `q` key was pressed, break from the loop
                    if key == ord("q"):
                        break

                # if an output video file path has been supplied and the video
                # writer has not been initialized, do so now
                if args["output"] != "" and writer is None:
                    # initialize our video writer
                    fourcc = cv2.VideoWriter_fourcc(*"MJPG")
                    writer = cv2.VideoWriter(args["output"], fourcc, 25,
                                             (frame.shape[1], frame.shape[0]), True)

                # if the video writer is not None, write the frame to the output
                # video file
                if writer is not None:
                    writer.write(frame)
                #print(engine)
                if not engine:
                    print(stopwatch.elapsed)
######$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$



                
                if (len(results) >= VIOLATION_COUNT_SETTING):#change this to family, university, work numbers
                    print(len(results), 'detected')
                    if engine:
                        stopwatch = Stopwatch()
                        stopwatch.start()
                        print('time',stopwatch.elapsed)
                        
                        engine=False
                    if(stopwatch.elapsed >VIOLATION_TIME_SETTING):
                        
                        print(len(results), "violations are detected at location:", ROOM_NAME)
                        #C:\Users\nouma\Desktop\Fab - SDM\Violaion Log\Room1
                        datee=datetime.datetime.now()
                        datee=datee.strftime("%D %T").replace(':','-').replace('/','-')
                        print(datee)
                        cv2.imwrite(str(f'Violaion Log/Room1/pic {ROOM_NAME} {datee}.jpg'),frame)
                        #this line lol
                        violation_count=len(results)
                        msg=str(f"{violation_count} violations detected at {ROOM_NAME} on {datee}. Please Check.")
                        send_violation_picture(lock, str(f'Violaion Log/Room1/pic {ROOM_NAME} {datee}.jpg'),msg)
                        engine=True

                        stopwatch.stop()
                        print('time',stopwatch.elapsed)
                else:
                    if (stopwatch.elapsed !=0):
                        #msg="Violation Has been cleared! No need to go."
                        #send_message(lock, msg)

                        engine=True
                        stopwatch.stop()


                        





######$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

#########################################################################################################################


            client_socket.close()
    except Exception as e:
        print(f"CLINET {addr} DISCONNECTED")
        print(e)
        pass

lock=threading.Lock()
while True:
    client_socket, addr = server_socket.accept()
    thread = threading.Thread(target=show_client, args=(addr, client_socket, lock))
    thread.start()
    print("TOTAL CLIENTS ", threading.activeCount() - 1)
