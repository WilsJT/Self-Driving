import cv2
import pytesseract
import pydirectinput
import time
import pickle

import pandas as pd
import numpy as np
import tensorflow as tf

from tesserocr import PyTessBaseAPI
from sklearn.preprocessing import StandardScaler
from PIL import ImageGrab

slopes = [np.tan(-np.pi/6), np.tan(-np.pi/4), np.tan(-np.pi/3), np.tan(np.pi/3), np.tan(np.pi/4), np.tan(np.pi/6)]
y_inter = [832, 1048, 1421, -345, 28, 243]
dim = np.array([[0, 275], [0, 570], [1020, 570], [1020, 275], [560, 260], [460, 260]])
pred = 0
speed = 40

pytesseract.pytesseract.tesseract_cmd = r"C:\Users\wilso\AppData\Local\Programs\Tesseract-OCR\tesseract.exe"

# Template of lines corresponding to angles
template = cv2.imread("./template.jpg", cv2.IMREAD_GRAYSCALE)

# Scaler for distances
scaler = StandardScaler()

# Load your model
model = tf.keras.models.load_model("./model_b.h5")

def roi(img, dim):
    """
    Take the defined region of interest from an image

    Parameters
    ----------

    img : np.array
        Image to take region of interest
    dim : list
        Dimensions of the region of interest
    """

    mask = np.zeros_like(img)
    cv2.fillPoly(mask, dim, 255)
    return(cv2.bitwise_and(img, mask))

def closest_dist(pixels):
    """
    Find the closest points for each angle and calculate their distances.

    Parameters
    ----------

    pixels : np.array or list
        Pixels/points leftover after bitwise_and with the screen and template
    """

    # indices correspond to 30, 45, 60, 90, 120, 135, 150 degrees
    points = [(243, 1020), (28, 1020), (-345, 1020), (0, 510), (-345, 0), (28, 0), (243, 0)]
    dists = []

    for point in pixels:
        if (point[1] == 510):
            if (point[0] > points[3][0]):
                points[3] = point
            continue

        for i in range(6):
            if (i < 3):
                j = i
            else:
                j = i + 1
            pred = int(slopes[i]*point[1])+y_inter[i]
            if (point[0] in [pred, pred-1, pred+1]):
                if (point[0] > points[j][0]):
                    points[j] = point
                break

    dist = np.linalg.norm(points-np.full((7, 2), [538, 510]), axis=1).reshape(-1, 1)

    return(dist, np.array(points))

while True:
    # Grab game screen
    grab = ImageGrab.grab(bbox=(0, 27, 1020, 565))
    screen = np.array(grab)

    # Grab portion of the screen for speed
    grab = ImageGrab.grab(bbox=(828, 56, 904, 100))
    # test = np.array(grab)

    # Get speed with tesseract
    with PyTessBaseAPI(path='C:/Users/wilso/OneDrive/Desktop/Python/tessdata', psm=6, oem=3) as api:
        api.SetImage(grab)
        speed_str = api.GetUTF8Text()

    try:
        speed = int(speed_str)
    except:
        if (pred == 0):
            speed += 20
        elif (pred == 1 or pred == 7):
            speed += 10
        elif (pred == 2 or pred == 6):
            speed -= 5
        elif (pred == 3 or pred == 5):
            speed -= 15
        elif (pred == 4):
            speed -= 25

    # Convert color to gray
    image = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)

    # Define a region of interest
    masked = roi(image, [dim])

    # Detect edges
    edges = cv2.Canny(masked, 200, 300)
    # edges = cv2.GaussianBlur(edges, (5,5), 0)

    # Get pixels
    pixels = cv2.bitwise_and(edges, template)

    # Get distances
    dists, points = closest_dist(np.argwhere(pixels > 150))
    dists = scaler.fit_transform(dists)

    X = np.append(dists, speed).reshape(1, -1)

    pred = np.argmax(model.predict(X))
    print(f"Prediction: {pred}")

# Keyboard simulation
    # North
    if (pred == 0):
        pydirectinput.keyDown("w")
        time.sleep(0.05)
        pydirectinput.keyUp("w")
    # Northeast
    elif (pred == 1):
        pydirectinput.keyDown("d")
        pydirectinput.keyDown("w")
        time.sleep(0.05)

        pydirectinput.keyUp("d")
        pydirectinput.keyUp("w")

    # East
    elif (pred == 2):
        pydirectinput.keyDown("d")
        time.sleep(0.25)

        pydirectinput.keyUp("d")

    # Southeast
    elif (pred == 3):
        pydirectinput.keyDown("s")
        pydirectinput.keyDown("d")
        time.sleep(0.25)

        pydirectinput.keyUp("s")
        pydirectinput.keyUp("d")

    # South
    elif (pred == 4):
        pydirectinput.keyDown("s")
        time.sleep(0.25)
        pydirectinput.keyUp("s")

    # Southwest
    elif (pred == 5):
        pydirectinput.keyDown("s")
        pydirectinput.keyDown("a")
        time.sleep(0.25)

        pydirectinput.keyUp("s")
        pydirectinput.keyUp("a")

    # West
    elif (pred == 6):
        pydirectinput.keyDown("a")
        time.sleep(0.25)
        pydirectinput.keyUp("a")

    # Northwest
    elif (pred == 7):
        pydirectinput.keyDown("a")
        pydirectinput.keyDown("w")
        time.sleep(0.05)

        pydirectinput.keyUp("a")
        pydirectinput.keyUp("w")

    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break
