#coding:utf-8
import os
from PIL import Image

os.chdir('/Users/Ru/Desktop/erya/vcode-lib/vcode-cut')

threshold = 140
table = []
for i in range(256):
    if i < threshold:
        table.append(0)
    else:
        table.append(1)



# 降噪
def getverify(name):
    im = Image.open(name)
    imgry = im.convert('L')
    imgry.save('gray_'+name)
    out = imgry.point(table,'1')
    out.save('binary_'+name)

'''
在这里调用tesseract,return text
'''
