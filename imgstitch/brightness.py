#引入opencv模块
import cv2 as cv
#引入numpy模块
import numpy as np

# https://stackoverflow.com/questions/32609098/how-to-fast-change-image-brightness-with-python-opencv
def increase_brightness(img, value=30):
    hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)
    h, s, v = cv.split(hsv)
    v = cv.add(v,value)
    v[v > 255] = 255
    v[v < 0] = 0
    final_hsv = cv.merge((h, s, v))
    img = cv.cvtColor(final_hsv, cv.COLOR_HSV2BGR)
    print("Increase:", value)
    return img

#对比度亮度调整
def adjust_v(img, average_v_mean, my_mean):
    return increase_brightness(img, int(0 * (my_mean - average_v_mean)))

def get_mean_v(imgs):
    mean = 0
    means = []
    for img in imgs:
        dst = cv.cvtColor(img, cv.COLOR_RGB2HSV)
        m = np.mean(dst[:, :, 2])
        print(dst[:, :, 2])
        print("Mean:", m)
        mean += m
        means.append(m)
    mean /= len(imgs)
    print("Av mean:", mean)
    return mean, means

# 将图片亮度调整为相似
def merge_brightness(imgs):
    av, ms = get_mean_v(imgs)
    return [adjust_v(img, av, m) for img, m in zip(imgs, ms)]