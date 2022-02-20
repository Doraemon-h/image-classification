# _*_ coding=utf-8 _*_

from cv2 import cv2
import time
import os
import numpy as np
from scipy.stats.stats import  pearsonr
import json


ImageFormatSet=["jpeg", "jpg", "bmp", "png"]
FOLDER="./seg_test/"

def rgb2hsv(pixel):
    r, g, b = pixel[2]/255.0, pixel[1]/255.0, pixel[0]/255.0
    mx = max(r, g, b)
    mn = min(r, g, b)
    df = mx-mn
    if mx == mn:
        h = 0
    elif mx == r:
        h = (60 * ((g-b)/df) + 360) % 360
    elif mx == g:
        h = (60 * ((b-r)/df) + 120) % 360
    elif mx == b:
        h = (60 * ((r-g)/df) + 240) % 360
    if mx == 0:
        s = 0
    else:
        s = df/mx
    v = mx
    if(s <= 0.2):
        s = 0
    elif(s >=0.7):
        s = 2
    else:
        s = 1

    if(v <= 0.2):
        v = 0
    elif(v >=0.7):
        v = 2
    else:
        v = 1

    if(h <= 20 and h > 315):
        h = 0
    elif(h > 20 and h <=40):
        h = 1
    elif(h > 40 and h <=75):
        h = 2
    elif(h > 75 and h <=155):
        h = 3
    elif(h > 155 and h <=190):
        h = 4
    elif(h > 190 and h <=270):
        h = 5
    elif(h > 270 and h <=295):
        h = 6
    else:
        h = 7
    return [h, s, v]

def getColorVec(img):
    hei, width, channel=img.shape
    colorVec=[0 for e in range(0, 72)]
    i=0
    while(i<hei):
        j=0
        while(j<width):
            pixel=img[i][j]
            grade=rgb2hsv(pixel)
            index=grade[0]*9+grade[1]*3+grade[2]
            colorVec[index]+=1
            j+=1
        i+=1
    return colorVec

def getFileSuffix(filename):
    return os.path.splitext(filename)[-1][1:]


#读取folderPath下的所有文件
def readFileInCurrentFolder(folderPath):
    all=os.listdir(folderPath)
    files=[]
    for file in all:
        if not os.path.isdir(file) and getFileSuffix(file) in ImageFormatSet :
            files.append(file)
    return files


def WriteDb(filename):
    if filename!="":
        if getFileSuffix(filename) not in ImageFormatSet:
            return
        fileSet=[filename]
    else:
        FL=os.listdir(FOLDER)
        fileSet = []
        for i in range(0,len(FL)):
            fileSet.append(readFileInCurrentFolder(FOLDER+FL[i]))
    hsvlist=[]
    for i in range(0,len(FL)):
        for file in fileSet[i]:
            img=cv2.imread(FOLDER+FL[i]+'/'+file)
            if img.ndim !=3:
                raise RuntimeError("图像维数不为3")
            filestat=os.stat(FOLDER+FL[i]+'/'+file)

            size=filestat.st_size
            colorVec=getColorVec(img)
            colorVecstr=str()
            for one in colorVec:
                colorVecstr+=str(one)+","
            colorVecstr=colorVecstr.strip(',')

            toGetTuple=[file, size, FL[i], colorVecstr]
            hsvlist.append(toGetTuple)
    f=open("hsv.txt","w")
    hsvlist_json = json.dumps(hsvlist)
    f.writelines(hsvlist_json)
    f.close()


if __name__ == '__main__':
    filename=""
    WriteDb(filename)

