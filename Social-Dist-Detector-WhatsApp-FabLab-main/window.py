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
from tkinter import Tk, Label, font
from time import sleep
from random import random
from PIL import ImageTk,Image
import tkinter.font as tkFont
a = int(time.perf_counter())
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--input", type=str, default="",
	help="path to (optional) input video file")
ap.add_argument("-o", "--output", type=str, default="",
	help="path to (optional) output video file")
ap.add_argument("-d", "--display", type=int, default=1,
	help="whether or not output frame should be displayed")
args = vars(ap.parse_args())

# load the COCO class labels our YOLO model was trained on
labelsPath = os.path.sep.join([config.MODEL_PATH, "coco.names"])
LABELS = open(labelsPath).read().strip().split("\n")

# derive the paths to the YOLO weights and model configuration
yolo = 0
if yolo == 0:
    weightsPath = os.path.sep.join([config.MODEL_PATH, "yolov3.weights"])
    configPath = os.path.sep.join([config.MODEL_PATH, "yolov3.cfg"])

elif yolo == 1:
    weightsPath = os.path.sep.join([config.MODEL_PATH, "yolov3-tiny.weights"])
    configPath = os.path.sep.join([config.MODEL_PATH, "yolov3-tiny.cfg"])


# load our YOLO object detector trained on COCO dataset (80 classes)
print("[INFO] loading YOLO from disk...")
net = cv2.dnn.readNetFromDarknet(configPath, weightsPath)

# check if we are going to use GPU

	# set CUDA as the preferable backend and target
print("[INFO] setting preferable backend and target to CUDA...")
net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)

# determine only the *output* layer names that we need from YOLO
ln = net.getLayerNames()
ln = [ln[i[0] - 1] for i in net.getUnconnectedOutLayers()]

# initialize the video stream and pointer to output video file
print("[INFO] accessing video stream...")
###
###full screen size


class App:
    def __init__(self, window, window_title, video_source=0):
        ##########
        #Parameters
        global w, h, W, H,wCnt,hCnt,EMOJI_SIZE
        w, h = window.winfo_screenwidth(), window.winfo_screenheight()
        ###
        W=int
        H=int
        wCnt=300
        hCnt=100
        EMOJI_SIZE = int(wCnt/2)-15


        ##########
        window.attributes("-fullscreen", True)
        window.configure(bg='#f3711d')
        self.window = window
        self.window.title(window_title)
        self.video_source = video_source

        #############
        self.canvas = tkinter.Canvas(window, width = w-wCnt, height = h-hCnt)
        self.canvas.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)
        
        #counter for violations.
        self.label = Label(text=str(0),borderwidth=3, relief="raised")
        self.label.config(font=("Joker", 50))
        self.label.pack()
        #############
        
        # RIT SOCIAL DISTANCING DETECTOR TITLE
        self.title = Label(text=str(0))
        self.title = Label(text=str(0), borderwidth=3, relief="raised")
        self.title.config(font=("Joker", 40))
        self.title.pack()
        self.title['text'] = ""
        self.title.config(bg="#f3711d")
        self.title.configure(text=" FABLAB SOCIAL DISTANCING DETECTOR ")
        self.title.place(rely=0.05, relx=0.5, x=0, y=0, anchor=N)


        # PLEASE MAINTAIN SOCIAL DISTANCE
        self.social_dist = Label(text=str(0))
        self.social_dist = Label(text=str(0), borderwidth=3, relief="raised")
        self.social_dist.config(font=("Joker", 40))
        self.social_dist.pack()
        self.social_dist.config(bg="red")
        self.social_dist.configure(text="PLEASE MAINTAIN SOCIAL DISTANCE")
        self.social_dist.place(rely=0.05, relx=0.5, x=0, y=0, anchor=N)
        ####################################################################################################################################################
        # Name of Coders: Syed Izhan Hyder, Noman Sheikh

       
        ####################################################################################################################################################

        # EMOJI REFFERENCE
        # my_pic_happy = Image.open("images/happy_emoji.jpg")
        # resized_happy = my_pic_happy.resize((EMOJI_SIZE, EMOJI_SIZE*3), Image.ANTIALIAS)
        # new_pic_happy = ImageTk.PhotoImage(resized_happy)
        # self.panel_west_happy = Label(window, image=new_pic_happy)
        # self.panel_east_happy = Label(window, image=new_pic_happy)
        #
        # self.panel_west_happy.config(bg="#f3711d")
        # self.panel_west_happy.place(rely=0.5, relx=0.0, x=0, y=0, anchor=tkinter.W)
        #
        # self.panel_east_happy.config(bg="#f3711d")
        # self.panel_east_happy.place(rely=0.5, relx=1.0, x=0, y=0, anchor=tkinter.E)
        #
        # my_pic_sad = Image.open("images/saf_emoji.jpg")
        # resized_sad = my_pic_sad.resize((EMOJI_SIZE, EMOJI_SIZE*3), Image.ANTIALIAS)
        # new_pic_sad = ImageTk.PhotoImage(resized_sad)
        # self.panel_west_sad = Label(window, image=new_pic_sad)
        # self.panel_east_sad = Label(window, image=new_pic_sad)
        #
        # self.panel_west_sad.config(bg="#f3711d")
        # self.panel_west_sad.place(rely=0.5, relx=0.0, x=0, y=0, anchor=tkinter.W)
        # self.panel_east_sad.config(bg="#f3711d")
        # self.panel_east_sad.place(rely=0.5, relx=1.0, x=0, y=0, anchor=tkinter.E)

        # open video source (by default this will try to open the computer webcam)
        self.vid = MyVideoCapture(self.video_source)

        # Create a canvas that can fit the above video source size
        #self.canvas = tkinter.Canvas(window, width = self.vid.width, height = self.vid.height)

        window.update()
        # RIT LOGO
        #########
        # global logo_formula
        # logo_formula =  EMOJI_SIZE#int((w-self.title.winfo_width())/4)
        # my_pic_rit_logo  = Image.open("images/rit.jpeg")
        # resized_rit_logo  = my_pic_rit_logo .resize((logo_formula,logo_formula), Image.ANTIALIAS)
        # new_pic_rit_logo  = ImageTk.PhotoImage(resized_rit_logo )
        # self.panel_rit_logo  = Label(window, image=new_pic_rit_logo )
        # self.panel_rit_logo  = Label(window, image=new_pic_rit_logo )
        # self.panel_rit_logo .config(bg="#f3711d")
        # self.panel_rit_logo .place(rely=0.0, relx=0.0, x=0, y=0, anchor=tkinter.NW)
        #########
        
        # CODING ALPHA LOGO
        # #########
        # my_pic_cod_logo = Image.open("images/cod.jpg")
        # resized_cod_logo  = my_pic_cod_logo .resize((logo_formula,logo_formula), Image.ANTIALIAS)
        # new_pic_cod_logo  = ImageTk.PhotoImage(resized_cod_logo )
        # self.panel_cod_logo  = Label(window, image=new_pic_cod_logo )
        # self.panel_cod_logo  = Label(window, image=new_pic_cod_logo )
        # self.panel_cod_logo .config(bg="#f3711d")
        # self.panel_cod_logo .place(rely=0.0, relx=1.0, x=-0, y=0, anchor=tkinter.NE)
        # #########

        

        #########

         # Button that lets the user take a snapshot
        #self.btn_snapshot=tkinter.Button(window, text="Snapshot", width=50, command=self.snapshot)
        #self.btn_snapshot.pack(anchor=tkinter.CENTER, expand=True)
 
         # After it is called once, the update method will be automatically called every delay milliseconds
        self.delay = 15
        self.updatee()
        self.window.mainloop()


    def updatee(self):
        # Get a frame from the video source
        ret, frame, violations = self.vid.get_frame()

        self.label['text'] = str(violations)
        self.label.config(bg="#f3711d")

        self.label.configure(text=" Violations Detected: " + str(violations) + " ")
        # rely controls verital (y axis)
        # relx control bottom horizontal (x axis)
        self.label.place(rely=0.92, relx=0.5, x=0, y=0, anchor=CENTER)

        # print(1)
        # if violations < 1:
        #     self.panel_west_sad.lower()
        #     self.panel_east_sad.lower()
        #     self.panel_west_happy.lift()
        #     self.panel_east_happy.lift()
        #     self.social_dist.lower()
        #     self.title.lift()
        #
        #
        # else:
        #     self.panel_west_sad.lift()
        #     self.panel_east_sad.lift()
        #     self.panel_west_happy.lower()
        #     self.panel_east_happy.lower()
        #     self.title.lower()
        #     self.social_dist.lift()
        #
            

            

        self.label.update()

            

################################################

        
        if ret:
            image_CV = PIL.Image.fromarray(frame)    
            
            #width = w-550, height = h-295
            resized_CV  = image_CV.resize((w-wCnt,h-hCnt), Image.ANTIALIAS)

            self.photo = PIL.ImageTk.PhotoImage(resized_CV)
            self.canvas.create_image(0, 0, image = self.photo, anchor = tkinter.NW)
            self.canvas .config(bg="black")
        self.window.after(self.delay, self.updatee)


class MyVideoCapture:
    def __init__(self, video_source=1):
     # Open the video source
        #self.vid = cv2.VideoCapture(0)
        self.vid = cv2.VideoCapture('aa.mp4')
        if not self.vid.isOpened():
           raise ValueError("Unable to open video source", video_source)

        # Get video source width and height
        self.width = (1000)
        self.height = (700)

    def get_frame(self):
        if self.vid.isOpened():
            ret, frame = self.vid.read()
            if ret:
                # Return a boolean success flag and the current frame converted to BGR




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
                                        if D[i, j] < config.MIN_DISTANCE:
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
                        cv2.rectangle(frame, (startX, startY), (endX, endY), color, 2)
                        cv2.circle(frame, (cX, cY), 5, color, 1)

                # draw the total number of social distancing violations on the
                # output frame
                '''
                text = "Social Distancing Violations: {}".format(len(violate))
                 
                cv2.putText(frame, text, (10, frame.shape[0] - 25),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.85, (0, 0, 255), 3)
                '''
                # check to see if the output frame should be displayed to our
                # screen
                
                        #################################################################
                      
                # if an output video file path has been supplied and the video
                # writer has not been initialized, do so now
                                        # if the video writer is not None, write the frame to the output
                # video file
                            

                resized = cv2.resize(frame, (w,h), fx=0.5, fy=0.5, interpolation = cv2.INTER_LINEAR)

                return (ret, cv2.cvtColor(resized, cv2.COLOR_BGR2RGB),len(violate))
            else:
                return (ret, None)
        else:
            return (ret, None)
 
    # Release the video source when the object is destroyed
    def __del__(self):
        if self.vid.isOpened():
            self.vid.release()

 # Create a window and pass it to the Application object
App(tkinter.Tk(), "Tkinter and OpenCV")
