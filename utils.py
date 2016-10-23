# coding:utf-8
from PIL import Image
import colorsys
import os

# 识别图片RGB


def get_color(im):
    im = Image.open(im)
    im = im.convert('RGBA')

    # 生成缩略图，减少计算量，减小cpu压力
    im.thumbnail((200, 200))

    max_score = None
    dominant_color = None

    for count, (r, g, b, a) in im.getcolors(im.size[0] * im.size[1]):

        saturation = colorsys.rgb_to_hsv(r / 255.0, g / 255.0, b / 255.0)[1]
        y = min(abs(r * 2104 + g * 4130 + b * 802 + 4096 + 131072) >> 13, 235)
        y = (y - 16.0) / (235 - 16)
        score = (saturation + 0.1) * count
        if score > max_score:
            max_score = score
            dominant_color = (r, g, b)

    return dominant_color

# 切图


def cut_vcode(path, out_path, a, b, c, d):
    im = Image.open(path)

    im.getbbox()

    region = (a, b, c, d)

    cropImg = im.crop(region)

    cropImg.save(out_path)
