import ctypes
import os.path
import uuid
import cv2
import loader

# Uncomment the source you want to select;
# for file & rtsp don't forget to change the path in assets\configs\settings.json
VID_SOURCE = "USB_CAM"
# VID_SOURCE = "FILE"
# VID_SOURCE = "RTSP"

# Change to True if you need to flip image
NEED_FLIP = True

# Default width & height of the images
WIDTH = 720
HEIGHT = 640
jewellery = None
impose = None
mx = my = None
dw = dh = None


def update_impose():
    global impose, mx, my, dw, dh
    impose = jewellery["path"]
    mx, my = jewellery["x"], jewellery["y"]
    dw, dh = jewellery["dw"], jewellery["dh"]


def save_picture(curr_frame):
    # Create the output folder if not exists
    if not os.path.exists(loader.get_absolute_path("captures", True)):
        os.makedirs(loader.get_absolute_path("captures", True))

    filename = r"captures\Capture_"+str(uuid.uuid4())[:6]+".jpg"
    filename = loader.get_absolute_path(filename, True)
    # Get a unique filename
    while os.path.exists(filename):
        filename = r"captures\Capture_" + str(uuid.uuid4())[:6]+".jpg"
        filename = loader.get_absolute_path(filename, True)
    cv2.imwrite(filename, curr_frame)

if __name__ == "__main__":
    # Set window icon during .exe execution
    MY_APP_ID = "Jewellery Setter"  # arbitrary string
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(MY_APP_ID)
    
    # print(loader.get_source(VID_SOURCE))
    cam = cv2.VideoCapture(loader.get_source(VID_SOURCE))
    cv2.imshow("preview", loader.generate_loading_screen(HEIGHT, WIDTH))

    # Load the required files into memory
    cascade, jewelleries = loader.load_files()
    jewel_key_list = list(jewelleries)

    # Set the first jewellery as current jewellery in use
    curr_jewel_index = 0
    jewellery = jewelleries[jewel_key_list[curr_jewel_index]]
    impose = jewellery["path"]
    mx, my = jewellery["x"], jewellery["y"]
    dw, dh = jewellery["dw"], jewellery["dh"]

    # Start reading the frames from source
    # alpha = 0.9 # 0.0 to 1.0
    check, frame = cam.read()
    cv2.waitKey(2000)

    if check:
        # If able to read the source; start capturing frames
        while check:
            check, frame = cam.read()
            if not check:
                continue

            # If you need to flip the image horizontally;
            # just change the NEED_FLIP to True above in global variable section
            if NEED_FLIP:
                frame = cv2.flip(frame, 1)

            # Resize the frame
            frame = cv2.resize(frame, (WIDTH, HEIGHT))
            # cv2.imshow('preview', frame)

            # Detect available faces in frame
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            # you can change the scaleFactor & minNeighbors if required
            faces = cascade.detectMultiScale(gray, scaleFactor=1.8, minNeighbors=3)
            # for x, y, w, h in faces:
            #     frame = cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 255, 0), 2)

            # Show the filter, if only 1 face is found otherwise it may create inconsistency
            # You can try with multiple faces... here
            if len(faces) == 1:
                # Extract face location
                x, y, w, h = faces[0]

                # Adjust the jewelery to the face's placement
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2BGRA)
                fw, fh = int(w * dw), int(w * dh)
                new_impose = cv2.resize(impose, (fw, fh))

                # Super impose the jewellery over captured frame
                iw, ih, c = new_impose.shape
                for i in range(0, iw):
                    for j in range(0, ih):
                        if new_impose[i, j][3] != 0:
                            if y + i + h + my < HEIGHT and x + j + mx < WIDTH:
                                # print(y + i + h + my, x + j + mx)
                                frame[y + i + h + my, x + j + mx] = new_impose[i, j]

            # Display the final image
            cv2.imshow("preview", frame)

            # Set ESC key to quit the program
            k = cv2.waitKey(15)
            if k == 27:
                break

            # Goto next jewellery when d is pressed
            elif k == ord("D") or k == ord("d"):
                if curr_jewel_index + 1 != len(jewel_key_list):
                    curr_jewel_index += 1
                else:
                    curr_jewel_index = 0
                jewellery = jewelleries[jewel_key_list[curr_jewel_index]]
                update_impose()

            # Goto previous jewellery when a is pressed
            elif k == ord("A") or k == ord("a"):
                if curr_jewel_index - 1 < 0:
                    curr_jewel_index = len(jewel_key_list) - 1
                else:
                    curr_jewel_index -= 1
                jewellery = jewelleries[jewel_key_list[curr_jewel_index]]
                update_impose()

            # Save the picture when S is pressed
            elif k == ord("s") or k == ord("S"):
                save_picture(frame)

    else:
        print("Error: Can't read camera")

    cv2.destroyAllWindows()
    cam.release()
