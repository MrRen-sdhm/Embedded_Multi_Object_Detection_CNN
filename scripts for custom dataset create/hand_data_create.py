# coding:utf8

from imutils import paths
import vocxml
import deal_image
import numpy as np
import cv2
import random
import shutil
import os

label = 'hand'
logonum = 8
pathnum = 18

imgcnt = 0
zoom = 1.0

logo_name = 'hand0511-' + str(logonum) + '.png'
path_name = 'Back' + str(pathnum)
img_logo = cv2.imread('./logo/Handlogo/' + logo_name, cv2.IMREAD_COLOR)

imagePaths = sorted(list(paths.list_images('./Back/' + path_name)))

# 删除文件夹中当前内容
print "[INFO] empty folder ./JPEGImages/ and ./Annotations/"
shutil.rmtree("./JPEGImages/")
os.mkdir("./JPEGImages/")
shutil.rmtree("./Annotations/")
os.mkdir("./Annotations/")

# 打乱图像顺序
random.seed(42)
random.shuffle(imagePaths)

print "[INFO] deal with images..."

# 预览及缩放比例调节
while True:
    img_back = cv2.imread('./zhanlang.jpg', cv2.IMREAD_COLOR)
    img_back = cv2.resize(img_back, (520, 320))

    img_back_copy = img_back.copy()
    img_logo_copy = img_logo.copy()
    img_logo_copy = cv2.resize(img_logo.copy(), (0, 0), fx=zoom, fy=zoom,
                               interpolation=cv2.INTER_NEAREST)
    # img_logo_copy = deal_image.rotate(img_logo_copy)
    # img_logo_copy = deal_image.stretch(img_logo_copy)
    cv2.rectangle(img_back_copy, (0, 0), (320, 320), (0, 255, 0), 2)

    # 制作mask，二值化后进行腐蚀，从而缩小手部区域，减少黑点
    gray = cv2.cvtColor(img_logo_copy, cv2.COLOR_BGR2GRAY)
    # thresh = cv2.threshold(gray, 2, 255,
    #                        cv2.THRESH_BINARY)[1]
    _, contours, _ = cv2.findContours(
        gray, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if contours:
        maxcnt = max(contours, key=lambda x: cv2.contourArea(x))
        cv2.drawContours(gray, [maxcnt], -1, (255, 255, 255), -1)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    img_logo_mask = cv2.erode(gray, kernel)
    img_logo_mask1 = cv2.bitwise_not(img_logo_mask)

    Height_logo, Width_logo, channel = img_logo_copy.shape
    Height_back, Width_back, channel1 = img_back_copy.shape

    if Width_back - Width_logo >= 10 and Height_back - Height_logo >= 10:
        Locate_x = 0
        Locate_y = 0
        img_roi = img_back_copy[Locate_y:Locate_y + Height_logo,
                                Locate_x:Locate_x + Width_logo]

        img_res0 = cv2.bitwise_and(img_roi, img_roi, mask=img_logo_mask1)
        img_res1 = cv2.bitwise_and(
            img_logo_copy, img_logo_copy, mask=img_logo_mask)
        img_res2 = cv2.add(img_res0, img_res1)
        img_back_copy[Locate_y:Locate_y + Height_logo,
                      Locate_x:Locate_x + Width_logo] = img_res2[:, :]

        cv2.imshow("img_mask", img_logo_mask)
        cv2.imshow("img_res1", img_res1)
        cv2.imshow("img_res2", img_res2)
        cv2.imshow("img_output", img_back_copy)

        # cv2.imshow("img_mask1", img_logo_mask1)
        # cv2.imshow("img_bitwise_not", img_bitwise_not)
        # cv2.imshow("img_res0", img_res0)

        key = cv2.waitKey(0) & 0xFF
        if key == ord("q"):
            break
        elif key == ord("w"):
            zoom += 0.025
            print '[INFO] zoom :', zoom
        elif key == ord("s"):
            zoom -= 0.025
            print '[INFO] zoom :', zoom

    else:
        print "[INFO] zoom = " + str(zoom) + " is too large !"
        zoom -= 0.025

cv2.destroyAllWindows()

for backfileName in imagePaths:
    # logo左右翻转
    img_logo = cv2.flip(img_logo, 1)

    # 读取背景图像
    img_back = cv2.imread(backfileName, cv2.IMREAD_COLOR)
    img_back_copy = img_back.copy()
    if random.choice((0, 1)):
        img_back_copy = cv2.flip(img_back_copy, 1)

    # 对logo进行随机缩放
    range = random.choice((0.7, 0.8, 0.9, 1.0))
    img_logo_copy = cv2.resize(img_logo.copy(), (0, 0), fx=range * zoom, fy=range * zoom,
                               interpolation=cv2.INTER_NEAREST)
    img_logo_copy = deal_image.rotate(img_logo_copy)
    img_logo_copy = deal_image.stretch(img_logo_copy)

    # 制作mask，二值化后进行腐蚀，从而缩小手部区域，减少黑点
    gray = cv2.cvtColor(img_logo_copy, cv2.COLOR_BGR2GRAY)
    # thresh = cv2.threshold(gray, 2, 255,
    #                        cv2.THRESH_BINARY)[1]
    _, contours, _ = cv2.findContours(
        gray, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if contours:
        maxcnt = max(contours, key=lambda x: cv2.contourArea(x))
        cv2.drawContours(gray, [maxcnt], -1, (255, 255, 255), -1)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    img_logo_mask = cv2.erode(gray, kernel)
    img_logo_mask1 = cv2.bitwise_not(img_logo_mask)

    # 提取目标图片的ROI
    Height_logo, Width_logo, channel = img_logo_copy.shape
    Height_back, Width_back, channel1 = img_back_copy.shape

    if Width_back - Width_logo >= 10 and Height_back - Height_logo >= 10:
        # 生成随机位置，提取roi
        Locate_x = random.randrange(0, Width_back - Width_logo, 10)
        Locate_y = random.randrange(0, Height_back - Height_logo, 10)
        img_roi = img_back_copy[Locate_y:Locate_y + Height_logo,
                                Locate_x:Locate_x + Width_logo]

        # ROI和Logo图像融合
        img_res0 = cv2.bitwise_and(img_roi, img_roi, mask=img_logo_mask1)
        img_res1 = cv2.bitwise_and(
            img_logo_copy, img_logo_copy, mask=img_logo_mask)
        img_res2 = cv2.add(img_res0, img_res1)
        img_back_copy[Locate_y:Locate_y + Height_logo,
                      Locate_x:Locate_x + Width_logo] = img_res2[:, :]

        # 随机再处理图像
        img_back_copy = deal_image.RandOperate(img_back_copy)

        # 保存合成后的图像和对应的xml文件
        basename = os.path.basename(backfileName)
        spliname = os.path.splitext(basename)[0]
        logoname = os.path.splitext(logo_name)[0]
        outname = str(imgcnt) + '-' + logoname + '-' + spliname
        cv2.imwrite("./JPEGImages/" + outname + '.jpg', img_back_copy)
        vocxml.create_xml(xml_name=("./Annotations/" + outname + '.xml'),
                          filename=(outname + '.jpg'), labelname=label,
                          width=str(Width_back), height=str(Height_back),
                          xmin=str(Locate_x), ymin=str(Locate_y),
                          xmax=str(Locate_x + Width_logo), ymax=str(Locate_y + Height_logo))

        print '[INFO] ' + str(imgcnt + 1) + ' images have been processed'
        imgcnt += 1

    else:
        print "[INFO] range = " + str(range) + " is too large !"

print '\n', '[INFO] logo_name: ', logo_name, '\n', '[INFO] path_name: ', path_name, '\n'

# 复制文件到工程目录
autocopy = raw_input(
    "[INFO] Will copy images to the project folder [y] or [n] ?: ")
if autocopy == 'y':
    print '\n', '[INFO] images have been copy to the project folder', '\n'
    for file in os.listdir("./JPEGImages/"):
        shutil.copy("./JPEGImages/" + file,
                    "/home/sdhm/caffe/data/VOCdevkit2018/VOC2018/JPEGImages")
    for file in os.listdir("./Annotations/"):
        shutil.copy("./Annotations/" + file,
                    "/home/sdhm/caffe/data/VOCdevkit2018/VOC2018/Annotations")

cv2.destroyAllWindows()
