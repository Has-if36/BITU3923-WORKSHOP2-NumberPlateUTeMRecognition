# remove warning message
import os

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

# required library
import cv2
import sys
import numpy as np
from local_utils import detect_lp
from sklearn.preprocessing import LabelEncoder
from model import WPOD_NET, MOBILE_NET
from os.path import splitext
from keras.models import model_from_json
from keras.preprocessing.image import load_img, img_to_array
from sklearn.preprocessing import LabelEncoder

BASE_PATH = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))


class plate_recognition:
    def __init__(self, init_img_path='logo_dark_mode.png', wpod_net_path="model/wpod-net.json",
                 mobile_net_path="model/MobileNets_character_recognition.json",
                 label_path='model/license_character_classes.npy'):
        wpod_net_path = os.path.join(BASE_PATH, wpod_net_path)
        mobile_net_path = os.path.join(BASE_PATH, mobile_net_path)
        label_path = os.path.join(BASE_PATH, label_path)

        self.NO_DETECT = 'No Detected'
        self.img_path = os.path.join(BASE_PATH, init_img_path)
        # Load model architecture and weight
        self.wpod_net = WPOD_NET.load_model(wpod_net_path)
        # Load model architecture, weight
        self.mobile_net = MOBILE_NET.load_model(mobile_net_path)
        # Load labels
        self.labels = LabelEncoder()
        self.labels.classes_ = np.load(label_path)

        self.dummy_init_model()

    # To reduce the slow startup display effect
    def dummy_init_model(self, Dmax=608, Dmin=256, resize=True):
        image = cv2.imread(self.img_path)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = image / 255
        if resize:
            min_size = 0
            pix_range = []
            if image.shape[0] <= image.shape[1]:
                pix_range.append((0, image.shape[0]))
                lo_crop = round((image.shape[1] - image.shape[0]) / 2)
                hi_crop = lo_crop + image.shape[0]
                pix_range.append((lo_crop, hi_crop))
            elif image.shape[1] < image.shape[0]:
                lo_crop = round((image.shape[0] - image.shape[1]) / 2)
                hi_crop = lo_crop + image.shape[1]
                pix_range.append((lo_crop, hi_crop))
                pix_range.append((0, image.shape[1]))

            image = image[pix_range[0][0]:pix_range[0][1], pix_range[1][0]:pix_range[1][1]]
            image = cv2.resize(image, (224, 224))
        ratio = float(max(image.shape[:2])) / min(image.shape[:2])
        side = int(ratio * Dmin)
        bound_dim = min(side, Dmax)
        LpImg = []
        cor = None
        try:
            _, LpImg, _, cor = detect_lp(self.wpod_net, image, bound_dim, lp_threshold=0.5)
        except Exception as e:
            pass
            # print('Error:', e)

    def get_plate(self, image, Dmax=608, Dmin=256, resize=True):
        # img = cv2.imread(image)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = image / 255
        if resize:
            min_size = 0
            pix_range = []
            if image.shape[0] <= image.shape[1]:
                pix_range.append((0, image.shape[0]))
                lo_crop = round((image.shape[1] - image.shape[0]) / 2)
                hi_crop = lo_crop + image.shape[0]
                pix_range.append((lo_crop, hi_crop))
            elif image.shape[1] < image.shape[0]:
                lo_crop = round((image.shape[0] - image.shape[1]) / 2)
                hi_crop = lo_crop + image.shape[1]
                pix_range.append((lo_crop, hi_crop))
                pix_range.append((0, image.shape[1]))

            image = image[pix_range[0][0]:pix_range[0][1], pix_range[1][0]:pix_range[1][1]]
            image = cv2.resize(image, (224, 224))
            # cv2.imshow("Frame", image)
        ratio = float(max(image.shape[:2])) / min(image.shape[:2])
        side = int(ratio * Dmin)
        bound_dim = min(side, Dmax)
        LpImg = []
        cor = None
        try:
            _, LpImg, _, cor = detect_lp(self.wpod_net, image, bound_dim, lp_threshold=0.5)
        except Exception as e:
            # print('Error:', e)
            pass
        return image, LpImg, cor

    def read_plate(self, LpImg):
        if (len(LpImg)):  # check if there is at least car plate image
            # Scales, calculates absolute values, and converts the result to 8-bit.
            plate_image = cv2.convertScaleAbs(LpImg[0], alpha=(255.0))

            # convert to grayscale and blur the image
            img_gray = cv2.cvtColor(plate_image, cv2.COLOR_BGR2GRAY)
            img_blur = cv2.GaussianBlur(img_gray, (7, 7), 0)

            # Applied inversed thresh_binary
            img_binary = cv2.threshold(img_blur, 140, 255,
                                       cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

            kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
            img_dilate = cv2.morphologyEx(img_binary, cv2.MORPH_DILATE, kernel)

            cont, _ = cv2.findContours(img_binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            # Initialize a list which will be used to append charater image
            crop_characters = []

            # define standard width and height of character
            digit_w, digit_h = 30, 70

            for c in self.sort_contours(cont):
                (x, y, w, h) = cv2.boundingRect(c)
                ratio = h / w
                if 1 <= ratio <= 6.5:  # Only select contour with defined ratio
                    if h / plate_image.shape[
                        0] >= 0.3:  # Select contour which has the height larger than 30% of the plate
                        # Sperate number and give prediction
                        curr_num = img_dilate[y:y + h, x:x + w]
                        curr_num = cv2.resize(curr_num, dsize=(digit_w, digit_h))
                        _, curr_num = cv2.threshold(curr_num, 140, 255,
                                                    cv2.THRESH_BINARY + cv2.THRESH_OTSU)  # 220 - 225
                        crop_characters.append(curr_num)

            plate_number = ''
            for i, character in enumerate(crop_characters):
                title = np.array2string(MOBILE_NET.predict_from_model(character, self.mobile_net, self.labels))
                plate_number += title.strip("'[]")

            # print(plate_number)
            return plate_number
        else:
            return self.NO_DETECT

    # Create sort_contours() function to grab the contour of each digit from left to right
    def sort_contours(self, cnts):
        boundingBoxes = [cv2.boundingRect(c) for c in cnts]
        (cnts, boundingBoxes) = zip(*sorted(zip(cnts, boundingBoxes),
                                            key=lambda b: b[1][0], reverse=False))
        return cnts
