# coding:utf8
import cv2
import os
import numpy as np
import imutils
import random

imagePath = "./test.jpg"


def RandOperate(image):
    randnum = random.randint(0, 4)
    if randnum == 0:
        img = SaltNoisy(image)
    elif randnum == 1:
        img = BrightRatio(image)
    elif randnum == 2:
        img = DarkRatio(image)
    elif randnum == 3:
        img = ContrAdj(image)
    elif randnum == 4:
        img = cv2.GaussianBlur(image, (5, 1), 1)
    return img


def SaltNoisy(image):
    img = np.array(image)
    rows, cols, dims = img.shape
    for i in xrange(1500):
        x = np.random.randint(0, rows)
        y = np.random.randint(0, cols)
        img[x, y, :] = 255
    return img


def BrightRatio(image):
    bright = random.choice((1.0, 1.1))
    img = np.uint8(np.clip((bright * image + 10), 0, 255))
    return img


def DarkRatio(image):
    bright = random.choice((0.7, 0.8))
    img = np.uint8(np.clip((bright * image + 10), 0, 255))
    return img


def ContrAdj(image):
    rows, cols, channels = image.shape
    img = image.copy()
    a = random.choice((0.7, 0.71, 0.72))
    b = 100
    for i in range(rows):
        for j in range(cols):
            for c in range(3):
                color = image[i, j][c] * a + b
                if color > 255:
                    img[i, j][c] = 255
                elif color < 0:
                    img[i, j][c] = 0
    return img


def rotate(image):
    angle = random.choice((-15, 15, 0))
    rows, cols, channel = image.shape
    M = cv2.getRotationMatrix2D((cols / 2, rows / 2), angle, 1.0)
    img = cv2.warpAffine(image, M, (cols, rows))

    return img


def stretch(image):
    stretch = random.choice(([1.1, 1], [0.9, 1], [1, 1.1], [1, 0.9], [1, 1]))
    img = cv2.resize(image.copy(), (0, 0), fx=stretch[0], fy=stretch[1],
                     interpolation=cv2.INTER_NEAREST)
    return img


def main():
    image = cv2.imread(imagePath)
    cv2.imshow("image", image)

    # # 修改对比度
    Contr = ContrAdj(image)
    cv2.imshow("ContrAdj", Contr)
    # Stretch = stretch(image)
    # cv2.imshow("Stretch", Stretch)
    # # 添加椒盐噪声
    # SaltNoisy = SaltNoisy(image.copy())
    # cv2.imshow("SaltNoisy", SaltNoisy)
    # # 高斯模糊 (25,25,5)>(15,15,5)>(5,5,5)>(5,1,1)>(1,1,5)
    # Gauss = cv2.GaussianBlur(image.copy(), (5, 1), 1)
    # cv2.imshow("Gauss", Gauss)
    # # 左右反转
    # flip1 = cv2.flip(image.copy(), 1)
    # cv2.imshow("flip1", flip1)
    # # 上下反转
    # flip_1 = cv2.flip(image.copy(), -1)
    # cv2.imshow("flip_1", flip_1)
    # # 随机旋转
    # image = RandOperate(image)
    # cv2.imshow("RandOperate", image)
    # # 调亮
    # Bright = BrightRatio(image)
    # cv2.imshow("Bright", Bright)
    # # 调暗
    # Dark = DarkRatio(image)
    # cv2.imshow("Dark", Dark)

    cv2.waitKey(0)


if __name__ == "__main__":
    main()
