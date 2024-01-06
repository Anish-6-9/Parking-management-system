import cv2
import numpy as np
import cvzone
import pickle


cap = cv2.VideoCapture('easy1.mp4')

drawing = False
area_names = []

try:
    with open("parking", "rb") as f:
        data = pickle.load(f)
        polylines, area_names = data['polylines'], data['area_names']
except:
    polylines = []

points = []
current_name = " "


def draw(event, x, y, flags, para):
    # first check if key 'p' is pressed or not. if 'p'pressed then, runs draw().
    # if 'f' pressed exits this draw()
    global points, drawing, current_name
    if event == cv2.EVENT_LBUTTONDOWN and drawing:
        points.append((x, y))
    elif len(points) == 4 and drawing:
        print(points)
        current_name = input("Area Name: ")

        if current_name:
            area_names.append(current_name)
            polylines.append(np.array(points, np.int32))
            points = []


cv2.namedWindow('FRAME')
cv2.setMouseCallback('FRAME', draw)

while True:
    ret, frame = cap.read()
    if not ret:
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        continue
    frame = cv2.resize(frame, (950, 700))

    for i, polyline in enumerate(polylines):
        print(i)
        print(polyline)
        cv2.polylines(frame, [polyline], True, (0, 0, 255), 2)
        cvzone.putTextRect(frame, f'{area_names[i]}', tuple(polyline[0]), 1, 1)

    cv2.imshow('FRAME', frame)
    Key = cv2.waitKey(75) & 0xFF
    if Key == ord('s'):
        with open("parking", "wb") as f:
            data = {'polylines': polylines, 'area_names': area_names}
            pickle.dump(data, f)

    elif Key == ord('p'):
        # Enable drawing mode
        drawing = True
        # Reset points and current_name for the next area
        points = []
        current_name = " "

    elif Key == ord('f'):
        # Exit drawing mode
        drawing = False

    elif Key == ord('r'):  # Key for removing a polyline
        name_to_remove = input("Enter the name of the area to remove: ")
        for i, (polyline, name) in enumerate(zip(polylines, area_names)):
            if name == name_to_remove:
                del polylines[i]
                del area_names[i]
                print(f"Area '{name}' removed successfully.")
                break
        else:
            print("Area not found.")

    if Key == 27:
        break
cap.release()
cv2.destroyAllWindows()
