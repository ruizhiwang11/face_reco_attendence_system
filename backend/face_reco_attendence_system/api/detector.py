import cv2
import numpy as np
import os


class Detector():
    def __init__(self):

        self.input_yml = "trainer.yml"
        self.trainer_pwd = os.path.dirname(os.path.realpath(__file__))
        self.input_config_path = os.path.join(self.trainer_pwd, self.input_yml)
        self.recognizer = cv2.face.LBPHFaceRecognizer_create()
        self.recognizer.read(self.input_config_path)

    def detect(self, input_image):
        id, confidence = self.recognizer.predict(input_image)
        return id, confidence
