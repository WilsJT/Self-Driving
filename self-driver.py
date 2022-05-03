import cv2
import numpy as np
import timeit
from PIL import ImageGrab

# image = cv2.imread("./semicircle.png", cv2.IMREAD_COLOR)
# lines = cv2.imread("./lines.jpg", cv2.IMREAD_GRAYSCALE)
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
            cv2.line(img, (xy[0],xy[1]), (xy[2],xy[3]), (255,255,255), 1)



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
    # Grab screen
    grab = ImageGrab.grab(bbox=(0, 27, 1020, 565))
    screen = np.array(grab)

    # Convert color to gray
    image = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)

    # Define a region of interest
    dim = np.array([[0, 300], [0, 570], [1020, 570], [1020, 300], [510, 220], [410, 220]])
    masked = roi(image, [dim])

    # Detect edges
    edges = cv2.Canny(masked, 200, 300)
    edges = cv2.GaussianBlur(edges, (5,5), 0)

    # Get lanes

    # y = [88, 177, 266, 355, 444, 533, 622, 711]
    # for val in y:
    #     cv2.circle(screen, (val, 300), 5, (0, 0, 255), -1)
    # # edges = edges[:,0]
    temp = np.zeros_like(edges)

    lines = cv2.HoughLinesP(edges, 1, np.pi/180, 180, np.array([]), 200, 4)
    draw_lines(temp, lines)

    print(np.argwhere(temp != 0))
    # cv2.circle(screen, (np.where(edges != 0)[0][1], np.where(edges != 0)[1][1]), 5, (0,255,0), -1)
    cv2.imshow("edge", screen)
    cv2.imshow("canny", temp)
    # print(np.where(edges != 0))

    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break
