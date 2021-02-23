import cv2
import numpy as np
import pandas as pd
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
import os
from django.conf import settings
import csv

from train.dumpdata import f_name

frontalPath = os.path.join(
    settings.BASE_DIR, 'train', 'haarcascade_frontalface_alt.xml')


def match_face(imagePayload):
    # reading the data
    data = pd.read_csv(f_name).values

    # data partition
    X, Y = data[:, 1:-1], data[:, -1]
    X_train, X_test2, Y_train, Y_test = train_test_split(X, Y, train_size=0.80)
    A = data[:, 6]
    print(A)
    print(X_train)
    print(Y_train)
    # Knn function calling with k = 5
    model = KNeighborsClassifier(n_neighbors=8)

    model.fit(X_train, Y_train)

    imgPath = imagePayload['image']
    dpath = imgPath.split('/')
    f_path = os.path.join(settings.MEDIA_ROOT,
                          dpath[len(dpath) - 2], dpath[len(dpath) - 1])

    gray = cv2.imread(f_path, cv2.IMREAD_GRAYSCALE)
    classifier = cv2.CascadeClassifier(frontalPath)

    f_list = []

    faces = classifier.detectMultiScale(gray, 1.5, 5)
    X_test = []
    # if len(faces) == 0:
    #     return 'null'
    # Testing data
    for face in faces:
        x, y, w, h = face
        im_face = gray[y:y + h, x:x + w]
        im_face = cv2.resize(im_face, (100, 100))
        X_test.append(im_face.reshape(-1))
        print(X_test)

    response = model.predict(np.array(X_test))
    # sc = accuracy_score(Y_test, response)
    # print(sc)
    print(response)
    response2 = response.tolist()
    return response
