import cv2
import mediapipe as mp
import time
import math

font = cv2.FONT_HERSHEY_PLAIN

class handDetector():
    def __init__(self, mode = False, maxHands=2, modelComplexity=1, detectionCon=0.5, trackCon=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.modelComplex = modelComplexity
        self.trackCon = trackCon
        self.tipIds = [4, 8, 12, 16, 20]
        self.mpHands = mp.solutions.hands
        self.mpDraw = mp.solutions.drawing_utils
        self.hands = self.mpHands.Hands(self.mode, self.maxHands, self.modelComplex,
                                        self.detectionCon, self.trackCon)

    def findHands(self, img, draw = True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)

        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS)
        return img
    
    def findAllHands(self, img, draw=True, flipType=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)
        allHands = []
        h,w,c = img.shape
        
        if self.results.multi_hand_landmarks:
            for handType, handLms in zip(self.results.multi_handedness, self.results.multi_hand_landmarks):
                myHand = {}
                mylmList = []
                xList = []
                yList = []
                
                for id, lm in enumerate(handLms.landmark):
                    px, py = int(lm.x * w), int(lm.y * h)
                    mylmList.append([px,py])
                    xList.append(px)
                    yList.append(py)
                    
                ## Bounding Box
                xmin, xmax = min(xList), max(xList)
                ymin, ymax = min(yList), max(yList)
                boxW, boxH = xmax - xmin, ymax - ymin
                bbox = xmin, ymin, boxW, boxH
                cx, cy = bbox[0] + (bbox[2] // 2), \
                         bbox[1] + (bbox[3] // 2)
                
                ## Store the Data into Dictionary         
                myHand["lmList"] = mylmList
                myHand["bbox"] = bbox
                myHand["center"] = (cx,cy)
                
                if flipType:
                    if handType.classification[0].label == "Right":
                        myHand["type"] = "Left"
                    else:
                        myHand["type"] = "Right"
                else:
                    myHand["type"] = handType.classification[0].label
                allHands.append(myHand)
                
                ## Draw         
                if draw:
                    self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS)
                    cv2.rectangle(img, (bbox[0] -20, bbox[1] - 20), (bbox[0] + bbox[2] + 20, bbox[1] + bbox[3] + 20) , (255,0,255),6)
                    #cv2.putText(img,myHand["type"],(bbox[0] - 30, bbox[1] - 30),cv2.FONT_HERSHEY_PLAIN, 2,(255, 0, 255),2)     
        
        if draw:
            return allHands,img 
        else:
            return allHands
    
    def fingersUp(self, myHand):
        """
        Finds how many finger are open and returns in a list.
        Consider left and right hand separately
        :return: List of which fingers are up
        """
        myHandType = myHand["type"]
        myLmList = myHand["lmList"]
        if self.results.multi_hand_landmarks:
            fingers = [] 
            # Thumb
            if myHandType == "Right":   
                # Access 4 Thumb index and Cx      
                if myLmList[self.tipIds[0]][0] > myLmList[self.tipIds[0] - 1][0]:
                    fingers.append(1)
                else:
                    fingers.append(0)
            else:
                if myLmList[self.tipIds[0]][0] < myLmList[self.tipIds[0] - 1][0]:
                    fingers.append(1)
                else:
                    fingers.append(0)
                    
            # 4 Fingers
            for id in range(1, 5):         
                if myLmList[self.tipIds[id]][1] < myLmList[self.tipIds[id] - 2][1]:
                    fingers.append(1)
                else:
                    fingers.append(0)
        return fingers
    
    def findDistance(self,p1, p2, img=None):
        """
        Find the distance between two landmarks based on their
        index numbers.
        :param p1: Point1
        :param p2: Point2
        :param img: Image to draw on.
        :param draw: Flag to draw the output on the image.
        :return: Distance between the points
                 Image with output drawn
                 Line information
        """              
        x1, y1 = p1
        x2, y2 = p2
        cx, cy = (x1 + x2) //2, (y1 + y2) // 2
        length = math.hypot(x2-x1, y2-y1)
        info = (x1,y1,x2,y2,cx,cy)
        if img is not None:
            cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
            cv2.circle(img, (x2, y2), 15, (255, 0, 255), cv2.FILLED)
            cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), 3)
            cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)
            return length,info, img
        else:
            return length, info
        
    def findPosition(self, img, handNo=0, draw=True):
        lmList = []
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNo]
            print(myHand)
            for id, lm in enumerate(myHand.landmark):
                #print(id, lm)
                h,w,c = img.shape
                cx,cy = int(lm.x*w), int(lm.y*h)
                lmList.append([id, cx, cy])         
                #if draw:
                    #cv2.circle(img, (cx,cy), 15,(255,0,255),cv2.FILLED)
        return lmList

def main():
    pTime = 0
    cTime = 0
    cap = cv2.VideoCapture(0)
    detector = handDetector()

    while True:
        success, img = cap.read()
        img = detector.findHands(img)
        lmList = detector.findPosition(img)
        #print(lmList)

        if len(lmList) != 0:
            #print(lmList[4][1])
            cv2.circle(img, (lmList[4][1], lmList[4][2]), 15, (255, 0, 255), cv2.FILLED)

        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime

        cv2.putText(img, str(int(fps)), (10,70), font, 3, (255,0,255),4)

        cv2.imshow("Result",img)
        if cv2.waitKey(1) & 0XFF == ord('q'):
            break

if __name__ == "__main__":
    main()