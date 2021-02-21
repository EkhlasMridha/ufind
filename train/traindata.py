import cv2
import numpy as np
from train import dumpdata
import os

from django.conf import settings

f_list = []
frontalPath = os.path.join(
    settings.BASE_DIR, 'train', 'haarcascade_frontalface_default.xml')


def refreshModel(data):
    # print(data)
    classifier = cv2.CascadeClassifier(frontalPath)

    imgPath = data['image']
    dpath = imgPath.split('/')
    f_path = os.path.join(settings.MEDIA_ROOT,
                          dpath[len(dpath)-2], dpath[len(dpath)-1])

    img = cv2.imread(f_path, cv2.IMREAD_GRAYSCALE)

    while True:
        faces = classifier.detectMultiScale(img, 1.5, 5)
        faces = sorted(faces, key=lambda x: x[2] * x[3], reverse=True)
        faces = faces[:1]

        if len(faces) == 1:
            face = faces[0]
            x, y, w, h = face

            filtered_face = img[y:y + h, x:x + w]
            gray_face = cv2.resize(filtered_face, (100, 100))
            # print(len(f_list), type(gray_face), gray_face.shape)

            f_list.append(gray_face.reshape(-1))

        if len(f_list) == 6:
            break

    dumpdata.write(data['id'], np.array(f_list))
