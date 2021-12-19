import cv2
import pandas as pd
import matplotlib.pyplot as plt
import sklearn
import pickle
from PIL import Image
import os

path_folder = os.path.dirname(os.path.realpath(__file__))

predict_folder_path = os.path.join(path_folder, '..\\static\\predicts')
model_path = os.path.join(path_folder, ".\\final_models.pickle")
haar_path = os.path.join(path_folder, ".\\haarcascade_frontalface_default.xml")


def detect_gender(test_data_path, filename):

    models = pickle.load(
        open(model_path, 'rb'))

    # load all models
    haar = cv2.CascadeClassifier(haar_path)


    pca_50 = models['pca_50']
    best_model_svm = models['model_svm']
    mean = models['mean']

    gender = ['male', 'female']
    font = cv2.FONT_HERSHEY_SIMPLEX
    # step-1 : read the image
    img = cv2.imread(test_data_path)
    # step-2 : convert the image to gray scale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # crop the faces with the haar casscade classifier
    faces = haar.detectMultiScale(gray, 1.5, 3)
    for x, y, w, h in faces:
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)  # drawing rectangle
        roi = gray[y:y + h, x:x + w]  # croping the faces
        # step-4 : normalization to the range of [0,1]
        roi = roi / 255
        # step - 5 : resize the image to 100x100 pixel
        if roi.shape[0] > 100:
            roi_resize = cv2.resize(roi, (100, 100), cv2.INTER_AREA)
        else:
            roi_resize = cv2.resize(roi, (100, 100), cv2.INTER_CUBIC)
        # step-6 : flattening the image to 1x10000
        roi_reshape = roi_resize.reshape(1, 10000)
        # step-7 : substract with the mean
        roi_mean = roi_reshape - mean
        # step-8 : get eigen image
        eigen_image = pca_50.transform(roi_mean)
        # step-9 : pass the image to our model (svm)
        results = best_model_svm.predict_proba(eigen_image)[0]
        # step -10 :
        predict = results.argmax()
        score = results[predict]

        text = "%s :%0.2f" % (gender[predict], score)
        cv2.putText(img, text, (x + 12, y - 12), font, 1, (0, 225, 0), 4)
        cv2.imwrite("{}/{}".format(predict_folder_path,filename), img)


