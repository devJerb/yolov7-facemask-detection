# terminal command
# git clone https://github.com/devJerb/yolov7.git

# move inside the directory of yolov7

# terminal command
# cd yolov7
# pip install -r requirements.txt
# pip install roboflow

import pandas as pd
import numpy as np
import seaborn as sns
import os
import shutil
import xml.etree.ElementTree as ET
import glob

import json

from IPython.display import HTML
from base64 import b64encode

# terminal command
# wget https://github.com/WongKinYiu/yolov7/releases/download/v0.1/yolov7-e6e.pt

def xml_to_yolo_bbox(bbox, w, h):
    x_center = ((bbox[2] + bbox[0]) / 2) / w
    y_center = ((bbox[3] + bbox[1]) / 2) / h
    width = (bbox[2] - bbox[0]) / w

    height = (bbox[3] - bbox[1]) / h
    return [x_center, y_center, width, height]

def create_folder(path):
    if not os.path.exists(path):
        os.makedirs(path)

gdrive_path = '/content/drive/MyDrive/'
create_folder(f'{gdrive_path}yolov7/train/images')
create_folder(f'{gdrive_path}yolov7/train/labels')
create_folder(f'{gdrive_path}yolov7/val/images')
create_folder(f'{gdrive_path}yolov7/val/labels')
create_folder(f'{gdrive_path}yolov7/test/images')
create_folder(f'{gdrive_path}yolov7/test/labels')

img_folder = f'{gdrive_path}yolov7/images'
_, _, files = next(os.walk(img_folder))
pos = 0
for f in files:
        source_img = os.path.join(img_folder, f)
        if pos < 700:
            dest_folder = f'{gdrive_path}yolov7/train/'
        elif (pos >= 700 and pos < 800):
            dest_folder = f'{gdrive_path}yolov7/val/'
        else:
            dest_folder = f'{gdrive_path}yolov7/test/'
        destination_img = os.path.join(dest_folder,'images', f)
        shutil.copy(source_img, destination_img)
        # print(destination_img) # show every destination folder made

        # check for corresponding label
        label_file_basename = os.path.splitext(f)[0]
        label_source_file = f"{label_file_basename}.xml"
        label_dest_file = f"{label_file_basename}.txt"
        
        label_source_path = os.path.join('annotations', label_source_file)
        label_dest_path = os.path.join(dest_folder, 'labels', label_dest_file)
        # if file exists, copy it to target folder
        if os.path.exists(label_source_path):
             # parse the content of the xml file
            tree = ET.parse(label_source_path)
            root = tree.getroot()
            width = int(root.find("size").find("width").text)
            height = int(root.find("size").find("height").text)
            classes = ['with_mask', 'without_mask', 'mask_weared_incorrect']
            result = []
            for obj in root.findall('object'):
                label = obj.find("name").text
                # check for new classes and append to list
                index = classes.index(label)
                pil_bbox = [int(x.text) for x in obj.find("bndbox")]
                yolo_bbox = xml_to_yolo_bbox(pil_bbox, width, height)
                # convert data to string
                bbox_string = " ".join([str(x) for x in yolo_bbox])
                result.append(f"{index} {bbox_string}")
                if result:
                    # generate a YOLO format text file for each xml file
                    with open(label_dest_path, "w", encoding="utf-8") as f:
                        f.write("\n".join(result))
                        
        
        pos += 1

# terminal command
# python train.py --weights yolov7-e6e.pt --data data/masks.yaml --workers 1 --batch-size 4 --img 416 --cfg cfg/training/yolov7-masks.yaml --name yolov7 --epochs 50

# terminal command
# python detect.py --weights ./runs/train/yolov7/weights/best.pt --conf 0.4 --img-size 640 --source /test/images/maksssksksss83.png
