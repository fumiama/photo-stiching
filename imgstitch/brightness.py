#引入opencv模块
import cv2 as cv
#引入numpy模块
import numpy as np


#对比度亮度调整
def adjust_v(img, average_v_mean):
    dst = cv.cvtColor(img, cv.COLOR_RGB2HSV)
    my_mean = np.mean(dst[:, :, 2])
    dst[:, :, 2] = average_v_mean / my_mean * dst[:, :, 2]
    return cv.cvtColor(dst, cv.COLOR_HSV2RGB)

def get_mean_v(imgs):
    mean = 0
    for img in imgs:
        dst = cv.cvtColor(img, cv.COLOR_RGB2HSV)
        mean += np.mean(dst[:, :, 2])
    mean //= len(imgs)
    return mean

# 将图片亮度调整为相似
def merge_brightness(imgs):
    av = get_mean_v(imgs)
    return [adjust_v(img, av) for img in imgs]