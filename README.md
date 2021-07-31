# SocialDistanceDetector

Using computer vision we detect if 2 or more people are social distancing or not.

# Note

Install all the required dependencies from the requirements.txt file

```
pip install -r requirements.txt
```
If you are running the client on Windows, comment out the speak function on the client.py file
```

def speak():
  ...

```
Once done installing dependencies, open the whatsapp.py file.

Here on line 14, change the hostname to yours for instance in my case it is "syedi":
```
options.add_argument("--user-data-dir=C:\\Users\\<hostname>\\AppData\\Local\\Google\\Chrome\\User Data") # change the hostname

options.add_argument("--user-data-dir=C:\\Users\\syedi\\AppData\\Local\\Google\\Chrome\\User Data") # 

```

This program downloads only the yolov3 tiny, but you can install yolov3 from their website:

``` https://pjreddie.com/darknet/yolo ```
