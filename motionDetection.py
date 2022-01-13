import cv2
import numpy as np
import time

cap = cv2.VideoCapture(0)
# frame_width = int( cap.get(cv2.CAP_PROP_FRAME_WIDTH))
#
# frame_height =int( cap.get( cv2.CAP_PROP_FRAME_HEIGHT))

# fourcc = cv2.VideoWriter_fourcc('X','V','I','D')

# out = cv2.VideoWriter("output.avi", fourcc, 5.0, (1280,720))

ret, frame1 = cap.read()
# frame1 = frame1[0:480,0:100]
ret, frame2 = cap.read()
# frame2 = frame2[0:480,0:100]
# print(frame1.shape)

esik = 20


while cap.isOpened():
    # cv2.line(frame1, (100, 0), (100, 640), (255, 0, 0), 2)
    diff = cv2.absdiff(frame1, frame2)
    gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5,5), 0)
    _, thresh = cv2.threshold(blur, esik, 255, cv2.THRESH_BINARY)
    dilated = cv2.dilate(thresh, None, iterations=1)
    contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        (x, y, w, h) = cv2.boundingRect(contour)

        if cv2.contourArea(contour) < 900:
            continue
        cv2.rectangle(frame1, (x, y), (x+w, y+h), (0, 255, 255), 2)
        # cv2.putText(frame1, "Status: {}".format('Movement'), (10, 20), cv2.FONT_HERSHEY_SIMPLEX,1, (0, 0, 255), 3)
        cv2.drawContours(frame1, contours, -1, (0, 255, 0), 2)

    # image = cv2.resize(frame1, (1280,720))
    # out.write(image)
    cv2.imshow("feed", frame1)
    cv2.imshow("feed2",dilated)
    cv2.imshow("feed3",blur)
    cv2.imshow("feed4",thresh)
    # cv2.imshow("feed5",contours)
    # print(diff[0][0])
    # time.sleep(0.5)
    frame1 = frame2
    ret, frame2 = cap.read()
    # frame2 = frame2[0:480,0:100]

    if cv2.waitKey(33) == ord("a"):
        esik+=10
        print(esik)

    if cv2.waitKey(33) == ord("b"):
        esik-=10
        print(esik)

    if cv2.waitKey(40) == 27:
        break

cv2.destroyAllWindows()
cap.release()
# out.release()