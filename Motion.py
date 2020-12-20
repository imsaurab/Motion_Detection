import cv2, time, pandas
from datetime import datetime

first_frame= None    #take a variable of first frame as none
status_list= [None,None]
times=[]
df=pandas.DataFrame(columns=["start","end"]) #

video=cv2.VideoCapture(0)  # create a video capture object using web cam

while True:
    check,frame=video.read()
    status=0
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # convert frame colour to gray scale
    gray=cv2.GaussianBlur(gray,(21,21),0)  # convert gray frame to gausionblur

    if first_frame is None:  # check if first frame is none
        first_frame=gray     # save the gray img to first frame of the video
        continue



    delta_frame=cv2.absdiff(first_frame,gray) #calculate the diff. b/w 1st and other frames
    thresh_delta=cv2.threshold(delta_frame,30,255,cv2.THRESH_BINARY)[1] #provide a threshold value
    thresh_delta=cv2.dilate(thresh_delta,None,iterations=0)
    (cnts,_)=cv2.findContours(thresh_delta.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE) #define the countor area

    for contour in cnts:
        if cv2.contourArea(contour)<1000:
            continue
        (x,y,w,h)=cv2.boundingRect(contour)
        cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),3) #create rectangular box around the object in frame

    status_list.append(status)
    status_list=status_list[-2:]

    if status_list[-1]==1 and status_list[-2]==0:
        times.append(datetime.now())
    if status_list[-1]==0 and status_list[-2]==1:
        times.append(datetime.now())

    print(status_list)
    print(times)
    if status ==1:
        time.append(datetime.now())
        break

    for i in range(0,len(times),2):
        df=df.append({"start":times[i],"end":times[i+1]},ignore_index=True)

    df.to_csv("Times.csv")

    cv2.imshow('frame',frame)
    cv2.imshow('capture',gray)
    cv2.imshow('delta',delta_frame)
    cv2.imshow('thresh',thresh_delta)
    key = cv2.waitKey(1)
    if key == ord('b'):
        break

video.release()
cv2.destroyAllWindows()












