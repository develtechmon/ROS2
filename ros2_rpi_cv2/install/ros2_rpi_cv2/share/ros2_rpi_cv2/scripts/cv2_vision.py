import cv2

cap = cv2.VideoCapture(0)
while True:
    ret,frame = cap.read()

    cv2.imshow("Frame", frame)

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    print(gray)
    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
