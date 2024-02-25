import cv2
from pyzbar.pyzbar import decode
import subprocess

def execute_data(data):
    subprocess.run(data, shell=True)
c = ""
# Initialize the camera
cap = cv2.VideoCapture(0)

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Convert the frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Decode QR codes
    decoded_objects = decode(gray)

    # Display the frame
    cv2.imshow('frame', frame)

    # Iterate over all detected QR codes
    for obj in decoded_objects:
        print("Type:", obj.type)
        print("Data:", (obj.data.decode("utf-8")))
        c = c + obj.data.decode("utf-8")
        cap.release()
        # Execute the data
        execute_data(c)
        # Close the camera and exit
        
        cv2.destroyAllWindows()
        exit()

    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()
print(c)
# execute_data(c)


# # pip install zbarlight

# import cv2
# import pyzbar.pyzbar as pyzbar

# def scan_qr_code():
#     camera = cv2.VideoCapture(0)

#     while True:
#         # Capture frame-by-frame
#         ret, frame = camera.read()

#         # Convert the frame to grayscale
#         gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

#         # Use zbarlight to scan for QR codes
#         qr_code = pyzbar.decode('qrcode', frame)

#         # If a QR code is found, execute the Python script
#         if qr_code is not None:
#             # Decode the QR code content
#             qr_content = qr_code[0].decode('utf-8')

#             # Execute the Python script
#             exec(qr_content)

#             # Break out of the loop after executing the script
#             break

#         # Display the frame
#         cv2.imshow('QR Code Scanner', frame)

#         # Check for 'q' key to quit
#         if cv2.waitKey(1) & 0xFF == ord('q'):
#             break

#     # Release the camera and close OpenCV windows
#     camera.release()
#     cv2.destroyAllWindows()

# if __name__ == "__main__":
#     scan_qr_code()
