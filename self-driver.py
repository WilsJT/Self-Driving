import cv2
import numpy as np
import timeit
import pytesseract
from PIL import ImageGrab

pytesseract.pytesseract.tesseract_cmd = r"C:\Users\wilso\AppData\Local\Programs\Tesseract-OCR\tesseract.exe"

# Template of lines corresponding to angles
template = cv2.imread("./template.jpg", cv2.IMREAD_GRAYSCALE)

# Get the region of interest
def roi(img, dim):
    mask = np.zeros_like(img)
    cv2.fillPoly(mask, dim, 255)
    return(cv2.bitwise_and(img, mask))

# Draw lines from HoughLinesP
def draw_lines(img, lines):
    if (lines is not None):
        for line in lines:
            xy = line[0]
            cv2.line(img, (xy[0],xy[1]), (xy[2],xy[3]), (255,255,255), 1)

# Get the closest pixels along different angles and their distances
def closest_dist(pixels):
    # indices correspond to 30, 45, 60, 90, 120, 135, 150 degrees
    points = [(243, 1020), (28, 1020), (-345, 1020), (0, 510), (-345, 0), (28, 0), (243, 0)]
    dists = []

    for point in pixels:
        # 30
        m = np.tan(-np.pi/6)
        pred = int(m*point[1])+832
        if (point[0] in [pred, pred-1, pred+1]):
            if (point[0] > points[0][0]):
                points[0] = point
            continue

        # 45
        m = np.tan(-np.pi/4)
        pred = int(m*point[1])+1048
        if (point[0] in [pred, pred-1, pred+1]):
            if (point[0] > points[1][0]):
                points[1] = point
            continue

        # 60
        m = np.tan(-np.pi/3)
        pred = int(m*point[1])+1421
        if (point[0] in [pred, pred-1, pred+1]):
            if (point[0] > points[2][0]):
                points[2] = point
            continue

        # 90
        if (point[1] == 510):
            if (point[0] > points[3][0]):
                points[3] = point
            continue

        # 120
        m = np.tan(np.pi/3)
        pred = int(m*point[1])-345
        if (point[0] in [pred, pred-1, pred+1]):
            if (point[0] > points[4][0]):
                points[4] = point
            continue

        # 135
        m = np.tan(np.pi/4)
        pred = int(m*point[1])+28
        if (point[0] in [pred, pred-1, pred+1]):
            if (point[0] > points[5][0]):
                points[5] = point
            continue

        # 150
        m = np.tan(np.pi/6)
        pred = int(m*point[1])+243
        if (point[0] in [pred, pred-1, pred+1]):
            if (point[0] > points[6][0]):
                points[6] = point
            continue

    dist = np.linalg.norm(points-np.full((7, 2), [538, 510]), axis=1)

    return(dist, np.array(points))

# def closest_dist(mask):
#     points = np.argwhere(mask > 200)
#
#     pos = []
#     # 30 Degrees
#     for point in points:
#         m = np.tan(-np.pi/6)
#         pred = int(m*point[1])+1092
#         if (point[0] == pred or point[0] + 1 == pred or point[0] - 1 == pred):
#             pos.append(point)
#
#     # 45 Degrees
#     for point in points:
#         m = np.tan(-np.pi/4)
#         pred = int(m*point[1])+1092
#         if (point[0] == pred or point[0] + 1 == pred or point[0] - 1 == pred):
#             pos.append(point)
#
#     # 60 Degrees
#     for point in points:
#         m = np.tan(-np.pi/3)
#         pred = int(m*point[1])+1092
#         if (point[0] == pred or point[0] + 1 == pred or point[0] - 1 == pred):
#             pos.append(point)
#
#     # 120 Degrees
#     for point in points:
#         m = np.tan(np.pi/3)
#         pred = int(m*point[1])+1092
#         if (point[0] == pred or point[0] + 1 == pred or point[0] - 1 == pred):
#             pos.append(point)
#
#     # 1
#     for point in points:
#         m = np.tan(np.pi/4)
#         pred = int(m*point[1])+1092
#         if (point[0] == pred or point[0] + 1 == pred or point[0] - 1 == pred):
#             pos.append(point)
#
#     for point in points:
#         m = np.tan(np.pi/6)
#         pred = int(m*point[1])+1092
#         if (point[0] == pred or point[0] + 1 == pred or point[0] - 1 == pred):
#             pos.append(point)




# edges = cv2.Canny(image, 100, 200)
# # mask = np.zeros_like(edges)
# # cv2.line(mask, (410, 382), (0, -328), (255,255,255), 1)
# # cv2.line(mask, (410, 382), (410, 0), (255,255,255), 1)
# # cv2.line(mask, (410, 382), (820, -328), (255,255,255), 1)
#
# # masked = cv2.bitwise_and(edges, mask, 255)
# print(image.shape)
# print("BITWISE_AND")
# start = timeit.default_timer()
# mask = cv2.bitwise_and(edges, lines)
# end = timeit.default_timer()-start
# print(end)
# points = np.argwhere(mask > 200)
# print(points)
# # ys, xs = np.where(mask!=0)
# # a = [i for i in zip(xs, ys)]
# # # print(x, y)
# # # cv2.imwrite("lines.jpg", mask)
# # # print(xs, ys)
# #
# # print(a)
# print("FOR LOOPS")
# start = timeit.default_timer()
# pos = []
# for point in points:
#     m = np.tan(-np.pi/3)
#     pred = int(m*point[1])+1092
#     # print(point[0], pred)
#     if (point[0] == pred or point[0] + 1 == pred or point[0] - 1 == pred):
#         pos.append(point)
#
# for point in points:
#     m = np.tan(np.pi/3)
#     pred = int(m*(point[1]))-328
#     # print(point[0], pred)
#     if (point[0] == pred or point[0] + 1 == pred or point[0] - 1 == pred):
#         pos.append(point)
# end = timeit.default_timer()-start
# print(end)
#
# print(pos)
# curr = [100000, None]
# for point in pos:
#     dist = np.linalg.norm(point - np.array([382, 410]))
#     if (dist < curr[0]):
#         curr = [dist, point]
#
# print(curr)
#     # -point[0], m*point[1]+328)
#
#
#
# cv2.circle(image, (410, 82), 5, (0,255,0), -1)
# cv2.circle(image, (263, 128), 5, (255,0,0), -1)
# cv2.circle(image, (557, 128), 5, (0,0,255), -1)
# print(points)

while True:
    # Grab screen for lanes
    grab = ImageGrab.grab(bbox=(0, 27, 1020, 565))
    screen = np.array(grab)

    # Grab portion of the screen for speed
    grab = ImageGrab.grab(bbox=(828, 56, 904, 100))

    # Get speed with tesseract
    speed = pytesseract.image_to_string(grab, config="--psm 6")

    # Convert color to gray
    image = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)

    # Define a region of interest
    dim = np.array([[0, 300], [0, 570], [1020, 570], [1020, 300], [510, 220], [410, 220]])
    masked = roi(image, [dim])

    # Detect edges
    edges = cv2.Canny(masked, 200, 300)
    edges = cv2.GaussianBlur(edges, (5,5), 0)

    # Get lanes
    lane = np.zeros_like(edges)
    lines = cv2.HoughLinesP(edges, 1, np.pi/180, 180, np.array([]), 225, 10)
    draw_lines(lane, lines)

    # Get pixels
    pixels = cv2.bitwise_and(lane, template)

    # Get distances
    dists, points = closest_dist(np.argwhere(pixels > 200))
    print(dists)

    # Draw points and lines to those points
    for point in points:
        cv2.line(screen, (510, 538), (point[1], point[0]), (0,255,0), 1)
        cv2.circle(screen, (point[1], point[0]), 5, (0,0,255), -1)


    cv2.imshow("lane", lane)
    cv2.imshow("image", screen)

    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break
