from flask import render_template, request
from flask import redirect, url_for
import web_app.app.utils as utils

from PIL import Image

import os

UPLAOD_FOLDER  = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..\\static\\uploads')


def getwidth(path):
    img = Image.open(path)
    size = img.size # width and height
    aspect = size[0]/size[1] # width / height
    w = 300 * aspect
    return int(w)


def base ():
    return render_template("base.html")



def index ():
    return render_template("index.html")


def faceapp():
    return render_template("faceapp.html")


def gender() :
    if request.method == 'POST' :
        f = request.files['image']
        filename  = f.filename
        path = os.path.join(UPLAOD_FOLDER, filename)
        f.save(path)
        w = getwidth(path)
        print("path of the uploaded image is ", path)
        utils.detect_gender(path, filename)
        return render_template("gender.html", fileupload=True, img_name=filename, w=w)
    return render_template("gender.html", fileupload=False)