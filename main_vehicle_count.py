import cv2
import imutils

class Box:
    def __init__(self, start_point, width_height):
        self.start_point = start_point
        self.end_point = (start_point[0] + width_height[0], start_point[1] + width_height[1])
        self.counter = 0
        self.frame_countdown = 0

    def overlap(self, start_point, end_point):
        if self.start_point[0] >= end_point[0] or self.end_point[0] <= start_point[0] or \
                self.start_point[1] >= end_point[1] or self.end_point[1] <= start_point[1]:
            return False
        else:
            return True


cap = cv2.VideoCapture('videos_images/object_detection_2.mp4')


# We will keep the last frame in order to see if there has been any movement
last_frame = None

# To build a text string with counting status
text = ""

# The boxes we want to count moving objects in
# Which ever vehicle crosses this line, the counter will increase to 1.
boxes = []
boxes.append(Box((0, 400), (700, 3)))
#boxes.append(Box((300, 350), (10, 80)))

while cap.isOpened():
    grabbed, frame = cap.read()
    if not grabbed:
        break

    # Scaling the frame
    frame = cv2.resize(frame , (640, 480))

    # Processing of frames are done in gray
    # scaling = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # We blur it to minimize reaction to small details
    gray = cv2.GaussianBlur(gray, (5, 5), 0)

    # Need to check if we have a lasqt_frame, if not get it
    if last_frame is None or last_frame.shape != gray.shape:
        last_frame = gray
        continue

    # Get the difference from last_frame
    delta_frame = cv2.absdiff(last_frame, gray)
    last_frame = gray
    # Have some threshold on what is enough movement
    thresh = cv2.threshold(delta_frame, 25, 255, cv2.THRESH_BINARY)[1]
    # This dilates with two iterations
    thresh = cv2.dilate(thresh, None, iterations=2)
    # Returns a list of objects
    contours = cv2.findContours(thresh.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    # Converts it
    contours = imutils.grab_contours(contours)
    #print(contours)

    # Loops over all objects found
    for contour in contours:
        # Skip if contour is small (can be adjusted)
        if cv2.contourArea(contour) < 700:
            continue
        #cv2.drawContours(frame, contour, -1, (0,255,0), 3)

        # Get's a bounding box and puts it on the frame
        (x, y, w, h) = cv2.boundingRect(contour)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # The text string we will build up
        text = "Vehicles Passing:"
        # Go through all the boxes
        for box in boxes:
            box.frame_countdown -= 1
            if box.overlap((x, y), (x + w, y + h)):
                if box.frame_countdown <= 0:
                    box.counter += 1
                # The number mzight be adjusted, it is just set based on my settings
                box.frame_countdown = 100
            text += " (" + str(box.counter) + " ," + str(box.frame_countdown) + ")"


 # Set the text string we build up
    cv2.putText(frame, text, (10, 40), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 0), 2)

    # Let's also insert the boxes
    for box in boxes:
        cv2.rectangle(frame, box.start_point, box.end_point, (0, 255, 255), 2)


    #cv2.imshow("Resize", frame)
    cv2.imshow("Car Counter", frame)
    #cv2.imshow('thresh', thresh)
    

    if cv2.waitKey(50) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()