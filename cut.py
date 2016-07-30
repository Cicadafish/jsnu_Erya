#coding:utf-8
from PIL import Image

# 切图
def cut_vcode(path,out_path,a,b,c,d):
    im = Image.open(path)

    im.getbbox()

    region = (a,b,c,d)

    cropImg = im.crop(region)

    cropImg.save(out_path)




# cut_vcode('./hah.png','./hah-cut.png',430,343,502,374)


# cut_vcode('./vcode-lib/sTJB6.png','./hah-cut.png',0,2,110,42)


# cut_vcode('./main.png','./main-cut.png',430,343,502,374)



# cut_vcode('./vcode-lib/52q10.png','./main-cut.png',405,202,500,237)