import numpy as np
from PIL import ImageGrab
from IPython.display import Image
import cv2
import time
import pyautogui
import math

RESOLUTION_WIDTH = 640
RESOLUTION_HEIGHT = 480

def draw_lanes(image, lines, color=[0, 255, 255], thickness=3):
    try:
        ys=[]
        for line in lines:
            for points in line:
                ys += [points[1], points[3]]
    except:
        pass
    return 1

def roi(screen, vertices) : # function to generate a regoin of interest with a set of vertices
    mask = np.zeros_like(screen) # returns np array filled with 0 size of screen
    cv2.fillPoly(mask, vertices, 255)
    masked = cv2.bitwise_and(screen, mask)
    return masked
    mask = np.zeros_like(screen)
    cv2.fillPoly(mask, vertices, 255)
    masked = cv2.bitwise_and(screen, mask)
    return masked

def draw_lines(screen, lines) :
    try :
        for line in lines :
            coords = line[0]
            cv2.line(screen, (coords[0], coords[1]), (coords[2], coords[3]), [255, 255, 255], 15)
    except :
        pass

def removeBackgorund(screen, lightPattern):
    screen32 = np.float32(screen)
    lightPattern32 = np.float32(lightPattern)
    np.clip(screen32, 0, 255)
    np.clip(lightPattern32, 0, 255)
    processed = (1 - screen32 / lightPattern32) * 255
    processed = np.float8(processed)
    return processed

def createBackground(screen):
    print("screen property: {} & {}".format(screen.shape[0], screen.shape[1]))
    processed = cv2.blur(screen, (screen.shape[0] / 3, screen.shape[1] / 3))
    return processed

def process_screen(screen, sigma = 0.333) :
    processed_screen = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY) # grayscale
    processed_screen = cv2.GaussianBlur(processed_screen, (3, 3), 0)
    median = np.median(processed_screen)
    lower_threshold = int(max(0, (1.0 - sigma) * median))
    higher_treshold = int(min(255, (1.0 - sigma) * median))
    processed_screen = cv2.Canny(processed_screen, threshold1 = lower_threshold,
                                threshold2 = higher_treshold, L2gradient = True) # edge detection

    # vertices = np.array([[0, 320], [0, 250], [240, 60], [400, 60], [640, 250], [640, 320]])
    vertices = np.array([[90, 60], [550, 60], [640, 200], [640, 320], [0, 320], [0, 200]])
    processed_screen = roi(processed_screen, [vertices])
    kernel = np.ones((3, 3), np.uint8)
    processed_screen = cv2.dilate(processed_screen, kernel)
    # processed_screen = cv2.GaussianBlur(processed_screen, (19, 19), 1)
    # HoughLinesP(image, rho, theta, threshold, min line length, max gap between lines)
    # returns an array of array containing lines
    lines = cv2.HoughLinesP(processed_screen, 1, np.pi / 180, 180, 20, 80)
    processed_screen = cv2.erode(processed_screen, kernel)
    # Leave out lines with gradient below 0.5 gradient
    processed_lines = []
    try :
        for line in  lines :
            # print(line)
            coords = line[0]
            # remove horizontal lines
            if abs((coords[3] - coords[1]) / (coords[2] - coords[0])) > 0.5 :
                processed_lines.append(line)
    except :
        pass
    if len(processed_lines) > 0:
        lines = processed_lines
    averageRadian = 0
    # try:
    totalRadian = 0
    for line in lines:
        coords = line[0]
        totalRadian += math.atan2(coords[3] - coords[1], coords[2] - coords[0])
    averageRadian = totalRadian / len(lines)
    print("averageRadian: {}".format(averageRadian))
    # except:
    #     pass

    draw_lines(processed_screen, lines)
    return processed_screen, lines

# def calculateMeanInverseGradient(lines):
#     lineCount = 0
#     lineGradientTotal = 0
#     meanInverseGradient = 0
#     try:
#         for line in lines:
#             coords = line[0]
#             gradient = (coords[3] - coords[1]) / (coords[2] - coords[0])
#             lineGradientTotal += gradient
#             lineCount += 1
#         meanInverseGradient = 1 / (-1 * (lineGradientTotal / lineCount))
#     except:
#         pass
#     return meanInverseGradient


def main() :
    #last_time = time.time()
    i = 0
    higher_treshold = 3
    while(True) :
        i += 1
        if i / 100000000 :
            i = 0
            if higher_treshold < 7 :
                higher_treshold += 2
            else :
                higher_treshold = 3

        screen = np.array(ImageGrab.grab(bbox = (0, 40, RESOLUTION_WIDTH, RESOLUTION_HEIGHT)))
        processed_screen, lines = process_screen(screen)
        kernel = np.ones((3, 3), np.uint8)

        cv2.imshow('window', processed_screen)
        # print(time.process_time())
        #last_time = time.time()
        # delete all screen captures after waiting a certain length of time?
        if cv2.waitKey(25) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break
        #Image(filename = 'edge-detection.png')

time.sleep(5)
main()
