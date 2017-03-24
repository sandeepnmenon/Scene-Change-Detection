
import sys
import numpy as np
import cv2

try:
	file_name=str(sys.argv[1])
	cap = cv2.VideoCapture(file_name)
except:
	print "File not found. Give valid file path as fisrt command line argument"
	sys.exit()
cnt=10


def LBP(frame):
    for i in range(len(frame)):
        for j in range(len(frame[0])):
            if i==0 or j==0 or i==len(frame)-1 or j==len(frame[0])-1:
                continue
            try: 
                gc=frame[i][j]
                newvalue=0
                if frame[i-1][j-1]>=gc:
                    newvalue+=1
                if frame[i-1][j]>=gc:
                    newvalue+=2
                if frame[i-1][j+1]>=gc:
                    newvalue+=4
                if frame[i][j+1]>=gc:
                    newvalue+=8
                if frame[i+1][j+1]>=gc:
                    newvalue+=16
                if frame[i+1][j]>=gc:
                    newvalue+=32
                if frame[i+1][j-1]>=gc:
                    newvalue+=64
                if frame[i][j-1]>=gc:
                    newvalue+=128

                frame[i][j]=newvalue
            except:
                print i,j
    return frame



def getCuts(cap):
    num=0
    aslbphd=[]
    cnt=0
    while(True):

        ret, frame = cap.read()
        # Our operations on the frame come here
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        disFrame=frame
        frame=LBP(gray)
        if num==0:
            prevframe=frame
            num+=1
            continue

        num+=1
        diff=0
        lbph=cv2.calcHist([frame],[0],None,[256],[0,256])
        prevlbph=cv2.calcHist([prevframe],[0],None,[256],[0,256])
        for i in range(256):
            diff+=abs(lbph[i]-prevlbph[i])

        if diff[0]>=25000:
            cnt+=1
            print "CUT "+str(cnt)+" Detected at frame "+str(num)
        aslbphd.append(diff)
        prevframe=frame
        # Display the resulting frame
        cv2.imshow('frame',disFrame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    print num


getCuts(cap)





