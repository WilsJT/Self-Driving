import cv2
import numpy as np
from PIL import ImageGrab

# # image = cv2.imread("./Dog.jpg", cv2.IMREAD_GRAYSCALE)
# edges = cv2.Canny(image, 100, 140)
# lines = cv2.HoughLinesP(edges, 1, np.pi/180, 100, 5, 10)
# # for point in lines:
# #     print(point[0])
# print(lines.shape)
# print(lines[0])

def roi(img, dim):
    mask = np.zeros_like(img)
    cv2.fillPoly(mask, dim, 255)
    return(cv2.bitwise_and(img, mask))

def draw_lines(img, lines):
    if (lines is not None):
        for line in lines:
            xy = line[0]
            cv2.line(img, (xy[0],xy[1]), (xy[2],xy[3]), (255,255,255), 3)


while True:
    # cv2.imshow("Dog", image)
    grab = ImageGrab.grab(bbox=(0, 27, 890, 570))

    screen = np.array(grab)

    # Convert color to gray
    image = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)

    dim = np.array([[0, 300], [0, 570], [890, 570], [890, 300], [600, 200], [290, 200]])
    masked = roi(image, [dim])
    edges = cv2.Canny(masked, 200, 300)
    edges = cv2.GaussianBlur(edges, (5,5), 0)
    lines = cv2.HoughLinesP(edges, 1, np.pi/180, 180, np.array([]), 200, 7)
    draw_lines(edges, lines)
    cv2.imshow("edge", edges)
    # print(np.where(edges != 0))

    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break
