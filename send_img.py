# -*- coding: utf-8 -*-
"""
Created on Fri Apr  7 11:17:21 2023

@author: amy
"""

import cv2
from flask import Flask, make_response
import os

from turbojpeg import TurboJPEG

app = Flask(__name__)
image_focus = 14521.6


def load_turbojpeg():
    basePath = os.path.split(os.path.realpath(__file__))[0]
    TurboJPEGPath = basePath + '\\turbojpeg.dll'
    turbojpeg = TurboJPEG(TurboJPEGPath)
    return turbojpeg

turbojpeg = load_turbojpeg()


@app.route("/image")
def index():
    image = cv2.imread('./image/0010.jpg')
    #转换为JPEG格式
    jpeg = turbojpeg.encode(image)
    #创建response对象
    resp = make_response(jpeg)
    #设置response的headers对象
    resp.headers['Content-Type'] = 'image/jpeg'
    resp.headers['image-focus'] = image_focus
    return resp


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=8000)