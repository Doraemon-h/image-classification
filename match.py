# _*_ coding=utf-8 _*_
from math import sqrt
from cv2 import cv2
import time
import os
import numpy as np
from scipy.stats.stats import  pearsonr
import json

FOLDER="./seg_test/mountain/"
#显示匹配的条目数量
MATCH_ITEM_NUM=100

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

def query(filename):
    if filename=="":
        fileToProcess=input("输入子文件夹中图片的文件名")
    else:
        fileToProcess=filename

    if(not os.path.exists(FOLDER+fileToProcess)):
        raise RuntimeError("文件不存在")

    img=cv2.imread(FOLDER+fileToProcess)
    colorVec1=getColorVec(img)

    leastNearRInFive=0
    Rlist=[]
    namelist=[]
    init_str="k"
    for one in range(0, MATCH_ITEM_NUM):
        Rlist.append(0)
        namelist.append(init_str)
    b = open(r"hsv.txt", "r")
    hvslist = b.read()
    hvslist = json.loads(hvslist)
    count=1
    num = 0
    for l in hvslist:
        colorVec2=l[3].split(',')
        colorVec2=list(map(eval, colorVec2))
        R2=pearsonr(colorVec1, colorVec2)
        rela=R2[0]
            #R2=Bdistance(colorVec1, colorVec2)
            #rela=R2
            #忽略正负性
            #if abs(rela)>abs(leastNearRInFive):
            #考虑正负
        if rela>leastNearRInFive:
            index=0
            for one in Rlist:
                if rela >one:
                    Rlist.insert(index, rela)
                    Rlist.pop(MATCH_ITEM_NUM)
                    namelist.insert(index, l[0]+' '+l[2])
                    namelist.pop(MATCH_ITEM_NUM)
                    leastNearRInFive=Rlist[MATCH_ITEM_NUM-1]
                    break
                index+=1
        count+=1

    for one in range(0, MATCH_ITEM_NUM):
        print(namelist[one]+"\t\t"+str(float(Rlist[one])))
        if("mountain" in namelist[one]):
            num = num + 1

    print(num)


if __name__ == '__main__':
    query("20599.jpg")

