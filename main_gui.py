from tkinter import *
from binascii import b2a_base64
from pickle import FRAME
from tkinter import *
import cv2
import imutils
from tkinter.tix import Tree
from main_image_my_functions import *
from main_video_my_functions import *

root = Tk()
root.title("Object Detection, Tracking Using OpenCV and YOLOv5")

# GUI Logic
root.geometry("944x600")
root.minsize(944, 600)
root.maxsize(944, 600)


#Input Image for Vehicle Detection and Number Plate Extraction
def v_i():

   
    save_img=True  # set true when using only image file to save the image
    # when using image as input, lower the threshold value of image classification

    cap = cv2.imread('videos_images\demo_6.jpg')
    frame = cv2.resize(cap, frame_size)  # resizing image
    original_frame = frame.copy()
    frame, results = object_detection(frame) 
    print(results, 1)

    rider_list = []
    head_list = []
    number_list = []

    for result in results:
        x1,y1,x2,y2,cnf, clas = result
        if clas == 0:
            rider_list.append(result)
        elif clas == 1:
            head_list.append(result)
        elif clas == 2:
            number_list.append(result)
            #print(number_list)
        print(1, number_list)

    for rdr in rider_list:
        time_stamp = str(time.time())
        x1r, y1r, x2r, y2r, cnfr, clasr = rdr
        for hd in head_list:
            x1h, y1h, x2h, y2h, cnfh, clash = hd
            if inside_box([x1r,y1r,x2r,y2r], [x1h,y1h,x2h,y2h]): # if this head inside this rider bbox
                try:
                    head_img = original_frame[y1h:y2h, x1h:x2h]
                    helmet_present = img_classify(head_img)
                    print("rider ",helmet_present)
                except:
                    helmet_present[0] = None

                if  helmet_present[0] == True: # if helmet present
                    frame = cv2.rectangle(frame, (x1h, y1h), (x2h, y2h), (0,255,0), 1)
                    frame = cv2.putText(frame, f'{round(helmet_present[1],1)}', (x1h, y1h+40), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255), 1, cv2.LINE_AA)
                    frame = cv2.putText(frame, "Helmet Worn", (x1h, y1h+60), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255, 0), 1, cv2.LINE_AA)
                elif helmet_present[0] == None: # if helmet absent 
                    frame = cv2.rectangle(frame, (x1h, y1h), (x2h, y2h), (0, 255, 255), 1)
                    frame = cv2.putText(frame, f'{round(helmet_present[1],1)}', (x1h, y1h), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255), 1, cv2.LINE_AA)
                    frame = cv2.putText(frame, "Helmet Absent", (x1h, y1h+20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255), 1, cv2.LINE_AA)
                elif helmet_present[0] == False: # Poor prediction
                    frame = cv2.rectangle(frame, (x1h, y1h), (x2h, y2h), (0, 0, 255), 1)
                    frame = cv2.putText(frame, f'{round(helmet_present[1],1)}', (x1h, y1h+40), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255), 1, cv2.LINE_AA)
                    frame = cv2.putText(frame, "No Helmet", (x1h, y1h+60), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255), 1, cv2.LINE_AA)
                    print("false  .....")
                    try:
                        cv2.imwrite(f'riders_pictures/{time_stamp}.jpg', frame[y1r:y2r, x1r:x2r])
                    except:
                        print('could not save rider')

                    print('S',number_list)
                    for num in number_list:
                        x1_num, y1_num, x2_num, y2_num, conf_num, clas_num = num
                        if inside_box([x1r,y1r,x2r,y2r], [x1_num, y1_num, x2_num, y2_num]):
                            try:
                                num_img = original_frame[y1_num:y2_num, x1_num:x2_num]
                                cv2.imwrite(f'number_plates/{time_stamp}_{conf_num}.jpg', num_img)
                            except:
                                print('could not save number plate')
                                

    frame = cv2.resize(frame, (900, 450))  # resizing to fit in screen
    cv2.imshow('Frame', frame)							
    if save_img: #save img
        cv2.imwrite('saved_frame.jpg', frame)


    cv2.waitKey(0) & 0xFF == ord('q')
    cv2.destroyAllWindows()
    print('Execution completed')





# Input as video
def v_d2():

    source = r'videos_images\4k.mp4' 
    #source = 'videos_images\record.mkv' 
    #source = 'videos_images\vid1.mp4'


    save_video = True # want to save video? (when video as source)
    show_video=True # set true when using video file
    # when using image as input, lower the threshold value of image classification

    #saveing video as output
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter('output.avi', fourcc, 20.0, frame_size)

    cap = cv2.VideoCapture(source)
    while(cap.isOpened()):
        ret, frame = cap.read()
        if ret == True:
            frame = cv2.resize(frame, frame_size)  # resizing image
            orifinal_frame = frame.copy()
            frame, results = object_detection_2(frame) 

            rider_list = []
            head_list = []
            number_list = []

            for result in results:
                x1,y1,x2,y2,cnf, clas = result
                if clas == 0:
                    rider_list.append(result)
                elif clas == 1:
                    head_list.append(result)
                elif clas == 2:
                    number_list.append(result)

            for rdr in rider_list:
                time_stamp = str(time.time())
                x1r, y1r, x2r, y2r, cnfr, clasr = rdr
                for hd in head_list:
                    x1h, y1h, x2h, y2h, cnfh, clash = hd
                    if inside_box([x1r,y1r,x2r,y2r], [x1h,y1h,x2h,y2h]): # if this head inside this rider bbox
                        try:
                            head_img = orifinal_frame[y1h:y2h, x1h:x2h]
                            helmet_present = img_classify_2(head_img)
                        except:
                            helmet_present[0] = None

                        if  helmet_present[0] == True: # if helmet present
                            frame = cv2.rectangle(frame, (x1h, y1h), (x2h, y2h), (0,255,0), 1)
                            frame = cv2.putText(frame, f'{round(helmet_present[1],1)}', (x1h, y1h+40), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255), 1, cv2.LINE_AA)
                            frame = cv2.putText(frame, "Helemt Worn", (x1h, y1h), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 1, cv2.LINE_AA)
                        elif helmet_present[0] == None: # Poor prediction
                            frame = cv2.rectangle(frame, (x1h, y1h), (x2h, y2h), (0, 255, 255), 1)
                            frame = cv2.putText(frame, f'{round(helmet_present[1],1)}', (x1h, y1h), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255), 1, cv2.LINE_AA)
                            frame = cv2.putText(frame, "", (x1h, y1h+40), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255), 1, cv2.LINE_AA)
                        elif helmet_present[0] == False: # if helmet absent 
                            frame = cv2.rectangle(frame, (x1h, y1h), (x2h, y2h), (0, 0, 255), 1)
                            frame = cv2.putText(frame, f'{round(helmet_present[1],1)}', (x1h, y1h+40), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255), 1, cv2.LINE_AA)
                            frame = cv2.putText(frame, "No Helmet", (x1h, y1h+40), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255), 1, cv2.LINE_AA)
                            try:
                                cv2.imwrite(f'riders_pictures/{time_stamp}.jpg', frame[y1r:y2r, x1r:x2r])
                            except:
                                print('could not save rider')

                            for num in number_list:
                                x1_num, y1_num, x2_num, y2_num, conf_num, clas_num = num
                                if inside_box([x1r,y1r,x2r,y2r], [x1_num, y1_num, x2_num, y2_num]):
                                    try:
                                        num_img = orifinal_frame[y1_num:y2_num, x1_num:x2_num]
                                        cv2.imwrite(f'number_plates/{time_stamp}_{conf_num}.jpg', num_img)
                                    except:
                                        print('could not save number plate')
                                        
            if save_video: # save video
                out.write(frame)
            if show_video: # show video
                frame = cv2.resize(frame, (900, 450))  # resizing to fit in screen
                cv2.imshow('Frame', frame)


            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
                
        else:
            break

    cap.release()
    cv2.destroyAllWindows()
    print('Execution completed')






# Counting Number of Vehicles Crossing Deadline.
def vehicle_count():

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


    cap = cv2.VideoCapture('videos_images\object_detection.mp4')


    # We will keep the last frame in order to see if there has been any movement
    last_frame = None

    # To build a text string with counting status
    text = ""

    # The boxes we want to count moving objects in
    # Which ever vehicle crosses this line, the counter will increase to 1.
    boxes = []
    boxes.append(Box((0, 400), (700, 3)))

    while cap.isOpened():
        grabbed, frame = cap.read()
        if not grabbed:
            break

        # Scaling the frame
        frame = cv2.resize(frame , (640, 480))

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
    

        if cv2.waitKey(15) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()




# Tkinter Logic

label_1 = Label(text = "Welcome to Traffic Monitoring System", font = ("Times New Roman-bold", 30), bd=5, relief = SUNKEN, bg = "blue")
label_1.pack(side = TOP, padx=50)




frame = Frame(root)
frame.pack(side=TOP)




v_d = Label(frame,text="Vehicle Detection\nNumber Plate Extraction(Image as Input)", font=("Times New Roman",20), bd =3, relief = GROOVE)
v_d.pack(pady = 20)

b1 = Button(frame, text="Run", font=("Times New Roman",15), command = v_i)
b1.pack(pady =10)




v_c = Label(frame, text="Vehicle Detection\nNumber Plate Extraction(Video Input)", font=("Times New Roman",20), bd = 3, relief = GROOVE)
v_c.pack(pady = 20)

b2 = Button(frame, text="Run", font=("Times New Roman",15), command = v_d2)
b2.pack(pady=10)



v_c = Label(frame, text="Vehicles Crossing\nThrough the Deadline", font=("Times New Roman",20), bd = 3, relief = GROOVE)
v_c.pack(pady = 20)

b2 = Button(frame, text="Run", font=("Times New Roman",15), command = vehicle_count)
b2.pack(pady=10)



root.mainloop()