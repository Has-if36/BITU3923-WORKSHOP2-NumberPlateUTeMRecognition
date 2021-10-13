# 1. Install IP Webcam for phone
# 2. Run and start the server, make sure you're connected with Wi-Fe (shared with your PC), not mobile data
# 3. Use the IP address displayed on the bottom screen
# 4. On PC, you can put URL 'https://192.168.1.17:8080' in your browser to explore, make sure the server has started first

import cv2
import numpy as np
url = "https://192.168.1.17:8080/video"     # Replace w/ your IP Address of your phone
cap = cv2.VideoCapture(url)
while(True):
    camera, frame = cap.read()
    if frame is not None:
        cv2.imshow("Frame", frame)
    q = cv2.waitKey(1)
    if q==ord("q"):
        break
cv2.destroyAllWindows()