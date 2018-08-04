# delete the image and corresponding xml file in VOC data set

import os

img_delete_name = raw_input(
    "[INFO] Input the image name you want to detete : ")

basename = os.path.basename(img_delete_name)
spliname = os.path.splitext(basename)[0]

img_delete_path = "./JPEGImages/" + img_delete_name
xml_delete_path = "./Annotations/" + spliname + '.xml'

print '[INFO] Delete:', img_delete_path, xml_delete_path

os.remove(img_delete_path)
os.remove(xml_delete_path)
