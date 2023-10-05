# Getting Started

This is userguide on how to `enable` GUI interface in `Ubuntu VM Ware`.

## Step 1 - Run below Script

By default, when you run below script, the `GUI` won't appear.

```
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
```

## Step 2 - To solve this, you need to install below package first 
```
sudo apt-get install v4l-utils
```

## Step 3 - Change `USB` setting in `VMware`

To do this you can follow settings
1. Go to `Player` --> `Manage` --> `Virtual Machine Settings`
2. Then go to `USB Controller` and Change `USB Compatibility` to `USB 3.1`. By default, it's `USB2.0`.
3. Save and exit.

## Step 4 - Attach `CAM` to `VMware`

1. From `Removable Device` then Connect your `Webcam` name to `VMware`.
2. Please ensure to `disconnect` from `Host` First.

## Step 5 - Rerun the script again.

1. You can re-rerun the script again, and now you should be able to see your `CV2` GUI.
