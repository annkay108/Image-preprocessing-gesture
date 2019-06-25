import cv2
import numpy as np
import os

#list of string from 0 to 50
x = list(str(y).zfill(2) for y in range(6))

if not os.path.exists("gesture"):
    os.makedirs("gesture")
    for i in range(6):
        mode = str(i).zfill(2)
        os.makedirs("gesture/"+mode+"/")
    
def nothing(x):
    pass

cap = cv2.VideoCapture(0)

cv2.namedWindow("Trackbars")

cv2.createTrackbar("L - H", "Trackbars", 0, 179, nothing)
cv2.createTrackbar("L - S", "Trackbars", 0, 255, nothing)
cv2.createTrackbar("L - V", "Trackbars", 0, 255, nothing)
cv2.createTrackbar("U - H", "Trackbars", 179, 179, nothing)
cv2.createTrackbar("U - S", "Trackbars", 255, 255, nothing)
cv2.createTrackbar("U - V", "Trackbars", 255, 255, nothing)

while True:
    _, frame = cap.read()
    frame = cv2.flip(frame, 1)
    frame = cv2.resize(frame, (640, 480))
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # to get the exact lower and upper hsv value
    l_h = cv2.getTrackbarPos("L - H", "Trackbars")
    l_s = cv2.getTrackbarPos("L - S", "Trackbars")
    l_v = cv2.getTrackbarPos("L - V", "Trackbars")
    u_h = cv2.getTrackbarPos("U - H", "Trackbars")
    u_s = cv2.getTrackbarPos("U - S", "Trackbars")
    u_v = cv2.getTrackbarPos("U - V", "Trackbars")

    lower = np.array([l_h, l_s, l_v])
    upper = np.array([u_h, u_s, u_v])
    mask = cv2.inRange(hsv, lower, upper)

    kernel = np.ones((5,5),np.uint8)
    erosion = cv2.erode(mask, kernel, iterations = 1)
    # dilation = cv2.dilate(mask,kernel, iterations = 1)

    median = cv2.medianBlur(erosion,15)

    #draw a rectangle
    x1 = int(0.6*frame.shape[1])
    y1 = 10
    x2 = frame.shape[1]-20
    y2 = int(0.4*frame.shape[1])
    cv2.rectangle(frame, (x1-1, y1-1), (x2+1, y2+1), (255,0,0) ,2)
    
    cv2.imshow("original",frame) # show original frame

    median = median[y1:y2, x1:x2]
    median = cv2.resize(median, (192, 192)) # image of 192x192 pixels

    # cv2.imshow("erosion",erosion)
    cv2.imshow("median",median)

    key1 = cv2.waitKey(1) & 0xFF
    
    if key1 & 0xFF == 27: # esc key
        break
    if key1!=255:
        key2 = cv2.waitKey(0) & 0xFF
        print(key2)
        key = chr(key1)+chr(key2)
        print(key)
        if key in x: # check if the key is in x or not
            cv2.imwrite("gesture/"+key+"/"+str(len(os.listdir("gesture/"+key+"/"))+1)+".jpg",median)
            print(key)

cap.release()
cv2.destroyAllWindows()